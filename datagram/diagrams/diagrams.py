import polars as pl
import re

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
        self.pk = self.__clean_column_name(primary_key)
        self.fk = self.__clean_column_name(foreign_keys)

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
    
    def __clean_column_name(self, cols: list[str]|str) -> list[str]|str:
        """Clean column(s) from special characters as they are not allowed in mermaid syntax."""
        if isinstance(cols, list):
            return [
                (re.sub(r"[!@%^&*+><//.]","",c))
                .strip()
                .replace(" ","_")
                .replace("$","Dollars")
                .replace("#","Number")
                for c in cols
            ]
        else:
            return (
                (re.sub(r"[!@%^&*+><//.]","",cols))
                .strip()
                .replace(" ","_")
                .replace("$","Dollars")
                .replace("#","Number")
            )
        
    def __build_attributes(self) -> list[str]:
        """Build the attributes string."""
        attributes = []
        cols = self.__clean_column_name(self.df.columns)

        attribute_schema = dict(zip(cols, self.df.dtypes))

        for a in attribute_schema:
            attribute_type = attribute_schema.get(a)
            attribute_name = a
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