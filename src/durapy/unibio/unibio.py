"""`UniBio` source — DNA/RNA/protein sequence utilities.

Sequences are handled as plain strings using the standard IUPAC nucleotide
alphabet. Functions normalize case and whitespace, and validate input by
default so mistakes are caught early instead of producing silent garbage.
"""

from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Alphabet and codon table
# --------------------------------------------------------------------------- #

DNA_BASES = frozenset("ACGT")
RNA_BASES = frozenset("ACGU")
AMBIGUOUS = frozenset("NRYWSKMBDHV")
VALID_DNA = DNA_BASES | AMBIGUOUS
VALID_RNA = RNA_BASES | AMBIGUOUS

DNA_COMPLEMENT = str.maketrans("ACGTN", "TGCAN")
RNA_COMPLEMENT = str.maketrans("ACGUN", "UGCAN")

# Amino acid -> space separated RNA codons (standard genetic code).
_AA_CODONS: dict[str, str] = {
    "F": "UUU UUC",
    "L": "UUA UUG CUU CUC CUA CUG",
    "I": "AUU AUC AUA",
    "M": "AUG",
    "V": "GUU GUC GUA GUG",
    "S": "UCU UCC UCA UCG AGU AGC",
    "P": "CCU CCC CCA CCG",
    "T": "ACU ACC ACA ACG",
    "A": "GCU GCC GCA GCG",
    "Y": "UAU UAC",
    "H": "CAU CAC",
    "Q": "CAA CAG",
    "N": "AAU AAC",
    "K": "AAA AAG",
    "D": "GAU GAC",
    "E": "GAA GAG",
    "C": "UGU UGC",
    "W": "UGG",
    "R": "CGU CGC CGA CGG AGA AGG",
    "G": "GGU GGC GGA GGG",
    "*": "UAA UAG UGA",
}

CODON_TABLE: dict[str, str] = {
    codon: amino_acid
    for amino_acid, codons in _AA_CODONS.items()
    for codon in codons.split()
}

START_CODON = "AUG"
STOP_CODONS = frozenset({"UAA", "UAG", "UGA"})

# Average nucleotide residue masses (Da) used for approximate sequence weights.
_DNA_RESIDUE_MASS = {"A": 313.21, "T": 304.2, "C": 289.18, "G": 329.21}
_RNA_RESIDUE_MASS = {"A": 329.21, "U": 306.17, "C": 305.18, "G": 345.21}
_WATER_MASS = 18.015
_PHOSPHATE_MASS = 79.975  # removed from a free 5' position


# --------------------------------------------------------------------------- #
# Normalization / validation
# --------------------------------------------------------------------------- #


def normalize(sequence: str) -> str:
    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string")
    return "".join(sequence.split()).upper()


def is_valid(sequence: str, kind: str = "dna") -> bool:
    """Return whether a sequence only contains valid bases for ``kind``."""
    kind = kind.lower()
    if kind not in {"dna", "rna"}:
        raise ValueError("kind must be 'dna' or 'rna'")
    allowed = VALID_DNA if kind == "dna" else VALID_RNA
    seq = normalize(sequence)
    return bool(seq) and set(seq) <= allowed


def validate(sequence: str, kind: str = "dna") -> str:
    """Return the normalized sequence, raising ``ValueError`` if invalid."""

    kind = kind.lower()
    if kind not in {"dna", "rna"}:
        raise ValueError("kind must be 'dna' or 'rna'")

    seq = normalize(sequence)

    if not seq:
        raise ValueError("Sequence cannot be empty")

    allowed = VALID_DNA if kind == "dna" else VALID_RNA
    invalid = sorted(set(seq) - allowed)

    if invalid:
        raise ValueError(f"Invalid {kind.upper()} base(s): {', '.join(invalid)}")
    return seq


def _as_rna(sequence: str, kind: str | None) -> str:
    """Return the sequence as RNA, auto-detecting DNA vs RNA when needed."""
    seq = normalize(sequence)
    if not seq:
        raise ValueError("Sequence cannot be empty")
    if kind is not None:
        kind = kind.lower()
        if kind == "dna":
            return validate(seq, "dna").replace("T", "U")
        if kind == "rna":
            return validate(seq, "rna")
        raise ValueError("kind must be 'dna', 'rna', or None")
    if "U" in seq and "T" in seq:
        raise ValueError("Sequence mixes DNA (T) and RNA (U) bases")
    if "U" in seq:
        return validate(seq, "rna")
    return validate(seq, "dna").replace("T", "U")


# --------------------------------------------------------------------------- #
# Sequence operations
# --------------------------------------------------------------------------- #


def complement(sequence: str, kind: str = "dna") -> str:
    """Return the Watson–Crick complement of a DNA or RNA sequence."""
    seq = validate(sequence, kind)
    return seq.translate(DNA_COMPLEMENT if kind.lower() == "dna" else RNA_COMPLEMENT)


def reverse_complement(sequence: str, kind: str = "dna") -> str:
    """Return the reverse complement of a sequence."""
    return complement(sequence, kind)[::-1]


def transcribe(sequence: str) -> str:
    """Transcribe a DNA coding strand to mRNA (`T` → `U`)."""
    return validate(sequence, "dna").replace("T", "U")


def reverse_transcribe(sequence: str) -> str:
    """Reverse-transcribe an RNA sequence to DNA (`U` → `T`)."""
    return validate(sequence, "rna").replace("U", "T")


def translate(sequence: str, kind: str | None = None, to_stop: bool = False) -> str:
    """Translate a nucleotide sequence into a protein (single-letter codes).

    `kind` is auto-detected when `None`. Translation proceeds codon by codon;
    a trailing partial codon is ignored. When `to_stop` is `True` the
    trailing stop codon is omitted from the result.
    """
    rna = _as_rna(sequence, kind)
    protein: list[str] = []
    for index in range(0, len(rna) - 2, 3):
        codon = rna[index : index + 3]
        amino_acid = CODON_TABLE.get(codon)
        if amino_acid is None:
            amino_acid = "X"  # ambiguous or unknown codon
        if amino_acid == "*":
            if to_stop:
                break
            protein.append("*")
            break
        protein.append(amino_acid)
    return "".join(protein)


def gc_content(sequence: str) -> float:
    """Return the GC content of a sequence as a percentage (0–100)."""
    seq = normalize(sequence)
    if not seq:
        raise ValueError("Sequence cannot be empty")
    gc = sum(1 for base in seq if base in "GC")
    return gc / len(seq) * 100.0


def count_nucleotides(sequence: str) -> dict[str, int]:
    """Return a count of each character in the sequence."""
    seq = normalize(sequence)
    if not seq:
        raise ValueError("Sequence cannot be empty")
    return {base: seq.count(base) for base in sorted(set(seq))}


def hamming_distance(first: str, second: str) -> int:
    """Return the number of positions at which two equal-length sequences differ."""
    a, b = normalize(first), normalize(second)
    if len(a) != len(b):
        raise ValueError("Sequences must be the same length for Hamming distance")
    return sum(x != y for x, y in zip(a, b))


def molecular_weight(
    sequence: str, kind: str = "dna", double_stranded: bool = False
) -> float:
    """Return an approximate molecular weight in Daltons.

    Uses average nucleotide residue masses for single strands. For double
    strands the weight is doubled. This is an estimate suitable for lab
    ballparks, not mass spectrometry.
    """
    seq = validate(sequence, kind)
    table = _DNA_RESIDUE_MASS if kind.lower() == "dna" else _RNA_RESIDUE_MASS
    weight = sum(table[base] for base in seq if base in table)
    # Subtract a water molecule per phosphodiester linkage, add one for the free 5' end.
    linkages = max(len([b for b in seq if b in table]) - 1, 0)
    weight -= linkages * _WATER_MASS
    weight += _PHOSPHATE_MASS
    if double_stranded:
        weight *= 2
    return weight


def melting_temperature(sequence: str, kind: str = "dna") -> float:
    """Estimate the duplex melting temperature (°C) of a DNA/RNA oligo.

    Uses the Wallace rule for sequences shorter than 14 bases and the
    GC-percentage formula otherwise.
    """
    seq = validate(sequence, kind)
    length = len(seq)
    gc = sum(1 for base in seq if base in "GC")
    if length < 14:
        at = sum(1 for base in seq if base in ("A", "T", "U"))
        return 2.0 * at + 4.0 * gc
    return 64.9 + 41.0 * (gc - 16.4) / length


@dataclass(frozen=True, slots=True)
class ORF:
    """An open reading frame in nucleotide coordinates (end exclusive)."""

    start: int
    end: int
    frame: int
    strand: str
    protein: str

    @property
    def length(self) -> int:
        """Nucleotide length of the ORF."""
        return self.end - self.start


def find_orfs(
    sequence: str,
    kind: str = "dna",
    min_amino_acids: int = 10,
    both_strands: bool = True,
) -> list[ORF]:
    """Find open reading frames (``AUG`` … stop codon) in a sequence.

    Returns ORFs on the forward strand and, when ``both_strands`` is ``True``,
    on the reverse strand (coordinates relative to the original sequence).
    """
    seq = validate(sequence, kind)
    if min_amino_acids < 1:
        raise ValueError("min_amino_acids must be at least 1")

    results: list[ORF] = []

    def scan(nucleotides: str, strand: str, reverse: bool) -> None:
        rna = nucleotides.replace("T", "U")
        for frame in range(3):
            index = frame
            while index + 3 <= len(rna):
                codon = rna[index : index + 3]
                if codon == START_CODON:
                    cursor = index
                    protein: list[str] = []
                    while cursor + 3 <= len(rna):
                        current = rna[cursor : cursor + 3]
                        cursor += 3
                        if current in STOP_CODONS:
                            break
                        protein.append(CODON_TABLE.get(current, "X"))
                    if len(protein) >= min_amino_acids:
                        start, end = index, cursor
                        if reverse:
                            start, end = len(seq) - end, len(seq) - index
                        results.append(ORF(start, end, frame, strand, "".join(protein)))
                    index = cursor
                else:
                    index += 3

    scan(seq, "+", False)
    if both_strands:
        scan(reverse_complement(seq, kind), "-", True)

    return results


__all__ = [
    "AMBIGUOUS",
    "CODON_TABLE",
    "DNA_BASES",
    "ORF",
    "RNA_BASES",
    "START_CODON",
    "STOP_CODONS",
    "VALID_DNA",
    "VALID_RNA",
    "complement",
    "count_nucleotides",
    "find_orfs",
    "gc_content",
    "hamming_distance",
    "is_valid",
    "melting_temperature",
    "molecular_weight",
    "normalize",
    "reverse_complement",
    "reverse_transcribe",
    "transcribe",
    "translate",
    "validate",
]
