import polars as pl

class ERDiagram:
    """Entity Relationship Diagram. This diagram describes the interrelations between data
    tables in a specific domain of knowledge."""

    def __init__(
        self,
        data: pl.DataFrame,
        entity_name: str,
        primary_key: str,
        foreign_keys: list[str]
    ):
        self.df = data
        self.name = entity_name
        self.pk = primary_key
        self.fk = foreign_keys

    def __str__(self) -> str:
        mermaid_diagram = ["erDiagram\n\t"]
        entity = [f"{self.name}", "{"]
        attributes = self.__build_attributes()
        closing = ["\n\t}"]
        
        mermaid_string = "".join(
            mermaid_diagram +
            entity + 
            attributes +
            closing
        )

        return mermaid_string
        
    
    def __build_attributes(self) -> list[str]:
        attributes = []
        attribute_schema = dict(zip(self.df.dtypes, self.df.columns))
        for a in attribute_schema:
            attribute_type = a
            attribute_name = attribute_schema.get(a)
            attribute = f"\n\t\t{attribute_type} {attribute_name}"

            if attribute_name == self.pk:
                pk = True
                attribute += " PK"
            else:
                pk = False

            if attribute_name in self.fk:
                if pk:
                    attribute += ", FK"
                else:
                    attribute += " FK"
            attributes.append(attribute)

        return attributes