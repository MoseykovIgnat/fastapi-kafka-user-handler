import xmltodict

from app.schemas.user import User


class GeneralUtils:
    @staticmethod
    def transform_xml_bytes_to_user_object(msg) -> User:
        parsed_value = xmltodict.parse(
            msg.value,
            process_namespaces=True,
            namespaces={"urn://www.example.com": None},
        )
        return User.model_validate(
            user_value["User"]
            if (user_value := parsed_value.get("Request"))
            else parsed_value["User"],
        )
