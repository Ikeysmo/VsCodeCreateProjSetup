import json

def create_task_dict():
    return {"version" : "2.0.0",
            "tasks" : [],
            }



def add_build_task(gdict, label = None, command = None, args = [], clear = True, dependsOn=None):
    t_dict = {
        "label" : label,
        "type" : "shell",
        "command" : command,
        "args" : args,
        "group" : {
            "kind" : "build",
            "isDefault" : True
        },
        "presentation" : {
            "clear" : clear
        }
    }

    if dependsOn:
        t_dict.update({"dependsOn" : [dependsOn]})

    return t_dict



def createFullOnTaskJson():
    base = create_task_dict()
    # create build task with sv
    base['tasks'].append(
        add_build_task(base, "Build", command="xvlog", args=["-sv", "-L", "uvm", "*.sv"],
                   clear = True, dependsOn=None)
    )
    base['tasks'].append(
        add_build_task(base, "Elaborate", command="xelab -sv top --debug typical --mt 8 --timescale 1ns/1ps",
                   clear = False, dependsOn="Build")
    )

    base['tasks'].append(
        add_build_task(base, "Simulate", command="xsim work.top -R",
                   clear = False, dependsOn="Elaborate")
    )

    base['tasks'].append(
        add_build_task(base, "Simulate (GUI)", command="xsim",
                       args=["work.top", "-gui", "--tclbatch", "simulate_batch.tcl"],
                   clear = False, dependsOn="Elaborate")
    )
    base['tasks'].append(
        add_build_task(base, "Generate Coverage", command="xcrg",
            args=[ "-dir", ".", "-report_dir", "./coverage_report", "-report_format", "html" ],
            clear = False)
    )

    base['tasks'].append(
        add_build_task(base, "Show Coverage", command="firefox",
                       args=["coverage_report/dashboard.html"],
                   clear = False, dependsOn="Generate Coverage")
    )
    return base


if __name__ == "__main__":
    print(json.dumps(createFullOnTaskJson()))
