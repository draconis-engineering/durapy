"""UniMath Exceptions module"""

class NonSquareShapeError(Exception):
    def __init__(self, shape: tuple[int, int]):
        self.shape = shape
        super().__init__(f"ShapeError: expected square matrix, got shape {shape}.")
