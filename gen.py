import json

# Take json input, see input.json to get a visual
#
# You specify configurations of radio button answers
# and for a given list of questions you then choose
# which configuration to use
#
# "Types" in input.json is where you specify the configurations you'll
# need for the questions. The options go in the options list and the
# options that will require a repair go under "repairable"
#
# The questions are a list of the question labels and then the type index
# for the config you want
#
# The one annoyance with this program is that the questions are
# put into json in the order their written which means if you have a single
# question that needs a different config it can get pretty verbose.
#
# Templating.json is all the stuff that seemed to be standard between all the radio
# so you're welcome to look at it, but probably won't need to change anything in it

def camel(s): #returns string in camelcase
    ret = ''.join(x for x in s.title() if not x.isspace())
    return ret[0].lower() + ret[1:]

def makeRadioOptions(RadioOptions): # makes the choices for a given question
    values = []
    for o in RadioOptions:
        option = {}
        option["label"] = o
        option["value"] = o
        option["shortcut"] = ""
        values.append(option)
    return values


def makeRadioComponent(lab, options, repairable): # assembles a single radio button component
    out = {}
    out["label"] = lab                          # add label
    out.update(preT)                            # add template lines between label and values
    out["values"] = makeRadioOptions(options)   # add values
    out["key"] = camel(lab)                 
    out["properties"] = {                       # add key and options that require repairs
        "repair": '^'.join(repairable)
    }
    out.update(postT)                           # add remaining templating line
    return(out)

inputJson = "input.json" # input file
outputJson = "output.json" # output file

data = json.load(open(inputJson, "r")) 
templating = json.load(open("templating.json", "r"))
preT = templating["pre"]
postT = templating["post"]

configs = data["types"]
questions = data["questions"]

components = []

for q in questions: # loops through questions and assembles a radio button component for each one
    conf = configs[q["type"]]
    for label in q["items"]:
        components.append(makeRadioComponent(label, conf["options"], conf["repairable"]))  #appends created radio button to component list

with open('output.json', "w+") as f:    # writes component list into json file which can be
    json.dump(components, f, indent=4)  # copied into questionPanel's component array