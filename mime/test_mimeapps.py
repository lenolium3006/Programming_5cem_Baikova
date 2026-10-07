from mimeapps import (
    read_associations,
    merge_associations,
    write_associations,
)


def test_read():
    associations = read_associations("example_mimeapps.list")

    assert associations["Default Applications"]["image/jpeg"] == [
        "eog.desktop"
    ]

    assert associations["Default Applications"]["application/pdf"] == [
        "evince.desktop"
    ]

    assert associations["Added Associations"]["image/jpeg"] == [
        "gimp.desktop",
        "eog.desktop"
    ]

    assert associations["Removed Associations"]["image/jpeg"] == [
        "old-viewer.desktop"
    ]


def test_merge():
    old = {
        "Default Applications": {
            "image/jpeg": ["old.desktop"],
            "application/pdf": ["evince.desktop"],
        }
    }

    new = {
        "Default Applications": {
            "image/jpeg": ["new.desktop"],
            "text/plain": ["code.desktop"],
        }
    }

    result = merge_associations(old, new)

    assert result == {
        "Default Applications": {
            "image/jpeg": ["new.desktop"],
            "application/pdf": ["evince.desktop"],
            "text/plain": ["code.desktop"],
        }
    }

    # Проверяем, что old не изменился
    assert old["Default Applications"]["image/jpeg"] == [
        "old.desktop"
    ]


def test_write():
    associations = {
        "Default Applications": {
            "image/jpeg": ["eog.desktop"],
        },

        "Added Associations": {
            "image/jpeg": [
                "gimp.desktop",
                "eog.desktop",
            ],
        },

        "Removed Associations": {},
    }

    write_associations(
        associations,
        "result_mimeapps.list"
    )

    # Проверяем результат повторным чтением
    result = read_associations("result_mimeapps.list")

    assert result == associations


if __name__ == "__main__":
    test_read()
    test_merge()
    test_write()

    print("Все тесты пройдены!")