"""Tests for the `durapy.unibio` module."""

import pytest

from durapy import unibio


# --------------------------------------------------------------------------- #
# Normalization and validation
# --------------------------------------------------------------------------- #


def test_normalize_strips_whitespace_and_uppercases():
    assert unibio.normalize("  atgc\n") == "ATGC"


def test_is_valid_and_validate():
    assert unibio.is_valid("ATGC", "dna")
    assert not unibio.is_valid("ATGC", "rna")
    assert unibio.is_valid("AUGC", "rna")
    assert unibio.is_valid("ANGT", "dna")  # IUPAC ambiguity code
    assert unibio.validate("atgc", "dna") == "ATGC"
    with pytest.raises(ValueError):
        unibio.validate("AXGT", "dna")
    with pytest.raises(ValueError):
        unibio.validate("", "dna")
    with pytest.raises(ValueError):
        unibio.validate("ATGC", "protein")


# --------------------------------------------------------------------------- #
# Complement / transcription / translation
# --------------------------------------------------------------------------- #


def test_complement_and_reverse_complement():
    assert unibio.complement("ATGC") == "TACG"
    assert unibio.reverse_complement("ATGC") == "GCAT"
    assert unibio.complement("AUGC", "rna") == "UACG"
    assert unibio.reverse_complement("AUGC", "rna") == "GCAU"


def test_transcription_round_trip():
    assert unibio.transcribe("ATGC") == "AUGC"
    assert unibio.reverse_transcribe("AUGC") == "ATGC"
    assert unibio.reverse_transcribe(unibio.transcribe("ACGTAC")) == "ACGTAC"


def test_translate_dna_and_rna():
    # ATG TTT TAA -> M F *
    assert unibio.translate("ATGTTTTAA") == "MF*"
    assert unibio.translate("ATGTTTTAA", to_stop=True) == "MF"
    assert unibio.translate("AUGUUUUAA") == "MF*"
    # Trailing partial codon is ignored.
    assert unibio.translate("ATGTT") == "M"
    # Ambiguous codon becomes X.
    assert unibio.translate("ATGNNN") == "MX"


def test_translate_rejects_mixed_t_and_u():
    with pytest.raises(ValueError):
        unibio.translate("AUGTTT")


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [("GGCC", 100.0), ("ATAT", 0.0), ("ATGC", 50.0), ("GATTACA", 200 / 7)],
)
def test_gc_content(sequence, expected):
    assert unibio.gc_content(sequence) == pytest.approx(expected)


def test_count_nucleotides():
    assert unibio.count_nucleotides("AATTC") == {"A": 2, "C": 1, "T": 2}


def test_hamming_distance():
    assert unibio.hamming_distance("ATGC", "ATCC") == 1
    assert unibio.hamming_distance("ATGC", "ATGC") == 0
    with pytest.raises(ValueError):
        unibio.hamming_distance("ATGC", "ATG")


def test_melting_temperature():
    # Wallace rule: 2*(A+T) + 4*(G+C)
    assert unibio.melting_temperature("ATGCATGCATGC") == pytest.approx(36.0)
    assert unibio.melting_temperature("ATGCATGCATGCATGCATGC") > 36.0


def test_molecular_weight():
    weight = unibio.molecular_weight("ATGCATGC")
    assert weight > 0
    assert unibio.molecular_weight("ATGCATGC", double_stranded=True) == pytest.approx(
        weight * 2
    )


# --------------------------------------------------------------------------- #
# ORF discovery
# --------------------------------------------------------------------------- #


def test_find_orfs_forward_strand():
    sequence = "AA" + "ATG" + "TTT" * 12 + "TAA"
    orfs = unibio.find_orfs(sequence, min_amino_acids=5, both_strands=False)
    assert len(orfs) == 1
    orf = orfs[0]
    assert orf.start == 2
    assert orf.frame == 2
    assert orf.strand == "+"
    assert orf.protein == "M" + "F" * 12
    assert orf.length == len(orf.protein) * 3 + 3  # includes start and stop codons


def test_find_orfs_respects_minimum_length():
    sequence = "ATGTTTTAA"
    assert unibio.find_orfs(sequence, min_amino_acids=5, both_strands=False) == []
    assert len(unibio.find_orfs(sequence, min_amino_acids=2, both_strands=False)) == 1


def test_find_orfs_both_strands():
    # The reverse complement of this sequence contains ATG ... TAA on the minus strand.
    sequence = unibio.reverse_complement("ATGTTTTAA")
    orfs = unibio.find_orfs(sequence, min_amino_acids=1, both_strands=True)
    minus = [orf for orf in orfs if orf.strand == "-"]
    assert minus
    assert minus[0].protein == "MF"  # ATG TTT TAA
