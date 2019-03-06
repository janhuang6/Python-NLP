import json

if __name__=="__main__":
    intent = "GetWeather"
    base_path = "C:\\projects\\datasets\\nlu-benchmark\\2017-06-custom-intent-engines\\"

    input_validate = base_path + intent + "\\validate_" + intent + ".json"
    input_train = base_path + intent + "\\train_" + intent + ".json"
    input_train_full = base_path + intent + "\\train_" + intent + "_full.json"

    output_validate = base_path + intent + "\\validate_" + intent + ".iob"
    output_train = base_path + intent + "\\train_" + intent + ".iob"
    output_train_full = base_path + intent + "\\train_" + intent + "_full.iob"

    io_validate = (input_validate, output_validate)
    io_train = (input_train, output_train)
    io_train_full = (input_train_full, output_train_full)

    ios = (io_validate, io_train, io_train_full)

    output_stats = open(base_path + intent + "\\" + intent + "_stats.txt", "w", encoding="utf-8")

    total_wc = 0
    entity_wc = {}

    for (input_file, output_file) in ios:
        with open(input_file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        output_iob = open(output_file, "w", encoding="utf-8")

        for utterance in data[intent]:
            origin = "BOS "
            label = "O"
            for item in utterance["data"]:
                text = item["text"]

                if text.isspace() or len(text) == 0:
                    continue
                text = text.replace('\n', ' ')
                text = text.replace('\t', ' ')

                if origin[len(origin)-1] != " " and text[0] != " ":
                    origin += " "
                origin += text
                split = text.split()
                if "entity" in item:
                    total_wc += 1
                    if item["entity"] not in entity_wc:
                        entity_wc[item["entity"]] = 0
                    entity_wc[item["entity"]] += 1
                    for x in range(len(split)):
                        if x == 0:
                            label += " B_" + item["entity"]
                        else:
                            label += " I_" + item["entity"]
                else:
                    for x in range(len(split)):
                        label += " O"
                        total_wc += 1

            label += " " + intent + "\n"

            origin += " EOS\t"

            output_iob.write(origin)
            output_iob.write(label)

        data_file.close()
        output_iob.close()

    output_stats.write("intent=\"{}\"\t".format(intent))
    output_stats.write("Total_words:{}\t".format(total_wc))
    slot_num = 1
    sum_wc = 0
    for key in entity_wc:
        output_stats.write("slot{}=\"{}\":{}({:.1%})\t".format(slot_num, key, entity_wc[key], float(entity_wc[key])/total_wc))
        sum_wc += entity_wc[key]
        slot_num += 1
    others_wc = total_wc-sum_wc
    output_stats.write("others={}({:.1%})\t".format(others_wc, float(others_wc)/total_wc))
    output_stats.write("\n")
    output_stats.close()
