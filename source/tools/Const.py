"""Module contains some constants for Application"""

from collections import OrderedDict

ROBOTICS_KITS = ["TRIK", "Lego EV3", "XML"]

ROBOTICS_KIT_TO_ID: dict = {"TRIK": "trikKitRobot", "Lego EV3": "ev3KitUsbRobot", "XML": "CUSTOM"}

"""
Keys that should be in dictionary for generating fields
"""
FIELD_GENERATOR_SETTINGS_KEYS: list = [
    "x",  # field size on X-direction
    "y",  # field size on Y-direction
    "valueExcersizeTimelimit",  # timelimit value
    "roboticsKit",  # robotics kit value from ROBOTICS_KITS
    "roboticsConfig", # robotics config if roboticsKit == "XML", contains str describing OrderedDict
    "valueLinePixelSize",  # line width size in pixels
    "valueMazeCellSize",  # maze cell size in TRIK Studio cells
    "valueLineCellSize",  # line cell size in TRIK Studio cells
    "valueColorLine",  # line color in hex format
]

"""
Ordered dictionary for XML generation:
Checks if all motors of EV3 robot had stopped
Before adding requires finish pattern in doc
To add this dictionary to XML field use:

doc['root']['constraints']['event'][0]['conditions'].update([('conditions', const.DICT_MOTOR_STOP_TRIK)])

XML code:
<conditions glue="and">
    <equals>
        <objectState object="robot1.M1.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.M2.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.M3.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.M4.power"/>
        <int value="0"/>
    </equals>
</conditions>
"""
DICT_MOTOR_STOP_TRIK = OrderedDict(
    [
        ("@glue", "and"),
        (
            "equals",
            [
                OrderedDict(
                    [
                        ("objectState", OrderedDict([("@object", "robot1.M1.power")])),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        ("objectState", OrderedDict([("@object", "robot1.M2.power")])),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        ("objectState", OrderedDict([("@object", "robot1.M3.power")])),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        ("objectState", OrderedDict([("@object", "robot1.M4.power")])),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
            ],
        ),
    ]
)

"""
Ordered dictionary for XML generation:
Checks if all motors of EV3 robot had stopped
Before adding requires finish pattern in doc
To add this dictionary to XML field use:

doc['root']['constraints']['event'][0]['conditions'].update([('conditions', const.DICT_MOTOR_STOP_EV3)])

XML code:
<conditions glue="and">
    <equals>
        <objectState object="robot1.A_out.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.B_out.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.C_out.power"/>
        <int value="0"/>
    </equals>
    <equals>
        <objectState object="robot1.D_out.power"/>
        <int value="0"/>
    </equals>
</conditions>
"""
DICT_MOTOR_STOP_EV3 = OrderedDict(
    [
        ("@glue", "and"),
        (
            "equals",
            [
                OrderedDict(
                    [
                        (
                            "objectState",
                            OrderedDict([("@object", "robot1.A_out.power")]),
                        ),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        (
                            "objectState",
                            OrderedDict([("@object", "robot1.B_out.power")]),
                        ),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        (
                            "objectState",
                            OrderedDict([("@object", "robot1.C_out.power")]),
                        ),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
                OrderedDict(
                    [
                        (
                            "objectState",
                            OrderedDict([("@object", "robot1.D_out.power")]),
                        ),
                        ("int", OrderedDict([("@value", "0")])),
                    ]
                ),
            ],
        ),
    ]
)

"""
Ordered dictionary for XML generation:
Addes finish check  pattern:
To complete task you should be in selected areas and print "finish" for 10 secs.
Parameter robot_id is "robot1"
To add this dictionary to XML field use doc['root']['constraints'].update([('event', const.DICT_FINISH_PATTERN)])

XML code:
<!-- Как только робот остановился и вывел на экран "Финиш", запускаем проверку таймера -->
<event id="wait_finish" settedUpInitially="true">
    <conditions glue="and">
        <greater>
            <objectState object="robot1.display.labels.size"/>
            <int value="0"/>
        </greater>
        <equals>
            <objectState object="robot1.display.labels.last.text"/>
            <string value="finish"/>
        </equals>
        <conditions glue="or"></conditions>
    </conditions>
    <trigger>
        <setUp id="check_timer"/>
    </trigger>
</event>

<!-- Предикат timer будет true по истечении времени в timeout, проверяем, что на экране все еще finish и success -->
<event id="check_timer" settedUpInitially="false">
    <conditions glue="and">
        <timer timeout="9000" forceDropOnTimeout="true"/>
        <greater>
            <objectState object="robot1.display.labels.size"/>
            <int value="0"/>
        </greater>
        <equals>
            <objectState object="robot1.display.labels.last.text"/>
            <string value="finish"/>
        </equals>
        <conditions glue="or"></conditions>
    </conditions>
    <trigger>
        <success />
    </trigger>
</event>
"""
DICT_FINISH_PATTERN = [
    OrderedDict(
        [
            ("@id", "wait_finish"),
            ("@settedUpInitially", "true"),
            (
                "conditions",
                OrderedDict(
                    [
                        ("@glue", "and"),
                        ("conditions", OrderedDict([("@glue", "or")])),
                        (
                            "greater",
                            OrderedDict(
                                [
                                    (
                                        "objectState",
                                        OrderedDict(
                                            [("@object", "robot1.display.labels.size")]
                                        ),
                                    ),
                                    ("int", OrderedDict([("@value", "0")])),
                                ]
                            ),
                        ),
                        (
                            "equals",
                            OrderedDict(
                                [
                                    (
                                        "objectState",
                                        OrderedDict(
                                            [
                                                (
                                                    "@object",
                                                    "robot1.display.labels.last.text",
                                                )
                                            ]
                                        ),
                                    ),
                                    ("string", OrderedDict([("@value", "finish")])),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            (
                "trigger",
                OrderedDict([("setUp", OrderedDict([("@id", "check_timer")]))]),
            ),
        ]
    ),
    OrderedDict(
        [
            ("@id", "check_timer"),
            ("@settedUpInitially", "false"),
            (
                "conditions",
                OrderedDict(
                    [
                        ("@glue", "and"),
                        (
                            "timer",
                            OrderedDict(
                                [("@timeout", "9000"), ("@forceDropOnTimeout", "true")]
                            ),
                        ),
                        ("conditions", OrderedDict([("@glue", "or")])),
                        (
                            "greater",
                            OrderedDict(
                                [
                                    (
                                        "objectState",
                                        OrderedDict(
                                            [("@object", "robot1.display.labels.size")]
                                        ),
                                    ),
                                    ("int", OrderedDict([("@value", "0")])),
                                ]
                            ),
                        ),
                        (
                            "equals",
                            OrderedDict(
                                [
                                    (
                                        "objectState",
                                        OrderedDict(
                                            [
                                                (
                                                    "@object",
                                                    "robot1.display.labels.last.text",
                                                )
                                            ]
                                        ),
                                    ),
                                    ("string", OrderedDict([("@value", "finish")])),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            ("trigger", OrderedDict([("success", None)])),
        ]
    ),
]

FIELD_START_FINISH_STR = '<?xml version="1.0" encoding="UTF-8"?>\
<root>\
        <world>\
                <background />\
                <walls>\
                </walls>\
                <skittles />\
                <balls />\
                <colorFields />\
                <images />\
                <regions>\
                </regions>\
        </world>\
        <robots>\
                <!-- Описание робота -->\
                <robot id="trikKitRobot" position="50:50" direction="0">\
                        <sensors></sensors>\
                        <startPosition id="{robot1}" x="75" y="75" direction="0" />\
                        <wheels left="M3###output###М3###" right="M4###output###М4###" />\
                </robot>\
        </robots>\
        <constraints>\
                <!-- Лимит на выполнение программы (30 секунд) -->\
                <timelimit value="999999000" />\
                <!-- Зональное ограничение на начало езды. Проверяется один раз в начале программы -->\
                <constraint checkOnce="true" failMessage="Робот должен находиться в синем квадрате перед запуском!">\
                        <conditions glue="or">\
                        </conditions>\
                </constraint>\
                <constraint failMessage="Робот заехал в запрещенную зону">\
                    <conditions glue="and"><not></not></conditions>\
                </constraint>\
        </constraints>\
</root>\
'

NOTIFICATION = (
    "<!--\nThis field was generated by maze-gui-gen\n"
    "Author: Lev Kozlov\n"
    "Contributors: iakov, AlexStrNik, anastasia-kornilova\n"
    "Licence: Apache 2.0\n"
    "website: https://lvjonok.github.io/maze-gui-gen/\n"
    "project page: https://github.com/lvjonok/maze-gui-gen\n"
    "Copyright © 2020 Lev Kozlov\n-->\n"
)
