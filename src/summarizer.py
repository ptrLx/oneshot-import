def summarize(counts):
    print("\n---------------- RESULT ----------------")
    import_count = counts.total() - counts["skipped"] - counts["error"]
    print(f"Found {counts.total()} images.")
    if import_count != counts.total():
        print(f"{import_count} can be imported.")

    if counts.total() == counts["metadata"] + counts["error"] + counts["skipped"]:
        print("All dates where read from EXIF metadata.")
    elif counts.total() == counts["android"] + counts["error"] + counts["skipped"]:
        print("All dates where read from Android file naming schema.")
    elif counts.total() == counts["ios"] + counts["error"] + counts["skipped"]:
        print("All dates where read from IOS file naming schema.")
    elif counts.total() == counts["oneshot"] + counts["error"] + counts["skipped"]:
        print("All dates where read from OneShot file naming schema.")
    elif counts.total() == counts["whatsapp"] + counts["error"] + counts["skipped"]:
        print("All dates where read from WhatsApp file naming schema.")
    else:
        print("Dates where read from:")
        if counts["metadata"]:
            print(f"  - Metadata: {counts['metadata']}")
        if counts["android"]:
            print(f"  - Android file naming schema: {counts['android']}")
        if counts["ios"]:
            print(f"  - IOS file naming schema: {counts['ios']}")
        if counts["oneshot"]:
            print(f"  - OneShot file naming schema: {counts['oneshot']}")
        if counts["whatsapp"]:
            print(f"  - WhatsApp file naming schema: {counts['whatsapp']}")

    if counts["skipped"]:
        print(
            f"{counts['skipped']} images where skipped because the date was already occupied."
        )
    if counts["error"]:
        print(
            f"{counts['error']} images where skipped because the date information was not readable."
        )
