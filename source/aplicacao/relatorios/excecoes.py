from typing import List, Sequence


class FormatoRelatorioInvalido(ValueError):
    def __init__(self, formatos_aceitos: Sequence[str]) -> None:
        self.formatos_aceitos: List[str] = list(formatos_aceitos)
        super().__init__(
            "formato de relatório não suportado; os formatos aceitos são "
            + " e ".join(self.formatos_aceitos)
        )
