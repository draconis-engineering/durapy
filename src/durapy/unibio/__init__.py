"""
The `DuraPy` `UniBio` module.

UniBio provides bioinformatics primitives for nucleotide and protein work:
sequence validation and normalization, complement/reverse-complement,
transcription and translation, GC content, melting temperature, approximate
molecular weight, and open reading frame discovery.
"""

from . import unibio
from .unibio import (
    AMBIGUOUS,
    CODON_TABLE,
    DNA_BASES,
    RNA_BASES,
    START_CODON,
    STOP_CODONS,
    VALID_DNA,
    VALID_RNA,
    ORF,
    complement,
    count_nucleotides,
    find_orfs,
    gc_content,
    hamming_distance,
    is_valid,
    melting_temperature,
    molecular_weight,
    normalize,
    reverse_complement,
    reverse_transcribe,
    transcribe,
    translate,
    validate,
)

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
    "unibio",
    "validate",
]
