from collections import Counter


class Summarizer:
    def __init__(self) -> None:
        self.summarization = ""

    def __sum_print(self, s: str):
        self.summarization += "\n" + s

    def summarize(self, counts: Counter) -> None:
        self.__sum_print("---------------- RESULT ----------------")

        import_count = counts.total() - counts["skipped"] - counts["error"]
        self.__sum_print(f"Images found: {counts.total()}")
        if import_count != counts.total():
            self.__sum_print(f"Imported: {import_count}")

        if import_count:
            if (
                counts.total()
                == counts["metadata"] + counts["error"] + counts["skipped"]
            ):
                self.__sum_print("All dates where read from EXIF metadata.")
            elif (
                counts.total()
                == counts["android"] + counts["error"] + counts["skipped"]
            ):
                self.__sum_print(
                    "All dates where read from Android file naming schema."
                )
            elif counts.total() == counts["ios"] + counts["error"] + counts["skipped"]:
                self.__sum_print("All dates where read from IOS file naming schema.")
            elif (
                counts.total()
                == counts["oneshot"] + counts["error"] + counts["skipped"]
            ):
                self.__sum_print(
                    "All dates where read from OneShot file naming schema."
                )
            elif (
                counts.total()
                == counts["whatsapp"] + counts["error"] + counts["skipped"]
            ):
                self.__sum_print(
                    "All dates where read from WhatsApp file naming schema."
                )
            else:
                self.__sum_print("Dates where read from:")
                if counts["metadata"]:
                    self.__sum_print(f"  - Metadata: {counts['metadata']}")
                if counts["android"]:
                    self.__sum_print(
                        f"  - Android file naming schema: {counts['android']}"
                    )
                if counts["ios"]:
                    self.__sum_print(f"  - IOS file naming schema: {counts['ios']}")
                if counts["oneshot"]:
                    self.__sum_print(
                        f"  - OneShot file naming schema: {counts['oneshot']}"
                    )
                if counts["whatsapp"]:
                    self.__sum_print(
                        f"  - WhatsApp file naming schema: {counts['whatsapp']}"
                    )

        if counts["skipped"]:
            self.__sum_print(
                f"Images skipped (date already occupied): {counts['skipped']}"
            )
        if counts["error"]:
            self.__sum_print(
                f"Images skipped (date information not readable): {counts['error']}"
            )

        return self.summarization
