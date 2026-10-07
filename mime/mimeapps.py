from copy import deepcopy


SECTIONS = [
    "Default Applications",
    "Added Associations",
    "Removed Associations",
]


def read_associations(path: str) -> dict:
    associations = {
        "Default Applications": {},
        "Added Associations": {},
        "Removed Associations": {},
    }

    current_section = None

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Пропускаем пустые строки
            if not line:
                continue

            # Пропускаем комментарии
            if line.startswith("#"):
                continue

            # Если встретили заголовок секции
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]

                if section in SECTIONS:
                    current_section = section
                else:
                    current_section = None

                continue

            # Если мы не внутри нужной секции
            if current_section is None:
                continue

            # В обычной записи обязательно должен быть =
            if "=" not in line:
                continue

            mime_type, applications = line.split("=", 1)

            mime_type = mime_type.strip()

            app_list = [
                app.strip()
                for app in applications.split(";")
                if app.strip()
            ]

            associations[current_section][mime_type] = app_list

    return associations


def merge_associations(old: dict, new: dict) -> dict:
    result = deepcopy(old)

    for section, mime_types in new.items():
        if section not in result:
            result[section] = {}

        for mime_type, applications in mime_types.items():
            result[section][mime_type] = applications.copy()

    return result


def write_associations(associations: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        for section in SECTIONS:
            section_data = associations.get(section, {})

            # Пустую секцию не записываем
            if not section_data:
                continue

            file.write(f"[{section}]\n")

            for mime_type, applications in section_data.items():
                app_string = ";".join(applications)
                file.write(f"{mime_type}={app_string}\n")

            file.write("\n")