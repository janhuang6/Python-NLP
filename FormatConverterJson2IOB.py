import json

if __name__=="__main__":
    with open("C:\\projects\\datasets\\nlu-benchmark\\2017-06-custom-intent-engines\\SearchScreeningEvent\\validate_SearchScreeningEvent.json", "r", encoding="utf-8") as data_file:
        data = json.load(data_file)

    intent = "SearchScreeningEvent"

    output_file = open("C:\\projects\\datasets\\nlu-benchmark\\2017-06-custom-intent-engines\\SearchScreeningEvent\\validate_SearchScreeningEvent.iob", "w", encoding="utf-8")

    for utterance in data[intent]:
        origin = "BOS "
        label = ""
        for item in utterance["data"]:
            text = item["text"]

            if origin[len(origin)-1] != " " and text[0] != " ":
                origin += " "
            origin += text
            if "entity" in item:
                split = text.split()
                for x in range(len(split)):
                    if x == 0:
                        if label != "":
                            label += " "
                        label += "B_" + item["entity"]
                    else:
                        if label != "":
                            label += " "
                        label += "I_" + item["entity"]
            else:
                split = text.split()
                for x in range(len(split)):
                    if label != "":
                        label += " "
                    label += "O"

        if label != "":
            label += " "
        label += "\t" + intent + "\n"

        origin += " EOS\t"
#        print(origin)
#        print(label)

        output_file.write(origin)
        output_file.write(label)
