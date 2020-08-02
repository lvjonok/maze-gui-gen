EMPTY_FIELD_STR = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\
<root>\
        <world>\
                <background></background>\
                <walls></walls>\
                <skittles></skittles>\
                <balls></balls>\
                <colorFields></colorFields>\
                <images></images>\
                <regions></regions>\
        </world>\
        <robots>\
                <robot direction=\"0\" id=\"trikKitRobot\" position=\"50:50\">\
                        <sensors></sensors>\
                        <startPosition direction=\"0\" id=\"{robot1}\" y=\"75\" x=\"75\"></startPosition>\
                        <wheels left=\"M4###output###М4###\" right=\"M3###output###М3###\"></wheels>\
                </robot>\
        </robots>\
</root>\
"

FIELD_START_FINISH_STR = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
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
                <robot id=\"trikKitRobot\" position=\"50:50\" direction=\"0\">\
                        <sensors>\
                        </sensors>\
                        <startPosition id=\"{robot1}\" x=\"75\" y=\"75\" direction=\"0\" />\
                        <wheels left=\"M3###output###М3###\" right=\"M4###output###М4###\" />\
                </robot>\
        </robots>\
        <constraints>\
                <!-- Лимит на выполнение программы (30 секунд) -->\
                <timelimit value=\"999999000\" />\
                <!-- Зональное ограничение на начало езды. Проверяется один раз в начале программы -->\
                <constraint checkOnce=\"true\" failMessage=\"Робот должен находиться в синем квадрате перед запуском!\">\
                        <conditions glue=\"or\">\
                        </conditions>\
                </constraint>\
                <!-- Событие, проверяющее не заехал ли робот в зону финиша -->\
                <event settedUpInitially=\"true\">\
                        <condition>\
                                <timer timeout=\"100\" forceDropOnTimeout=\"true\" />\
                        </condition>\
                        <trigger>\
                                <setUp id=\"finish checker\" />\
                        </trigger>\
                </event>\
                <event id=\"finish checker\" settedUpInitially=\"false\">\
                        <conditions glue=\"or\">\
                        </conditions>\
                        <trigger>\
                                <success />\
                        </trigger>\
                </event>\
        </constraints>\
</root>\
"


FIELD_START_STR = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
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
                <robot id=\"trikKitRobot\" position=\"50:50\" direction=\"0\">\
                        <sensors>\
                        </sensors>\
                        <startPosition id=\"{robot1}\" x=\"75\" y=\"75\" direction=\"0\" />\
                        <wheels left=\"M3###output###М3###\" right=\"M4###output###М4###\" />\
                </robot>\
        </robots>\
        <constraints>\
                <!-- Лимит на выполнение программы (30 секунд) -->\
                <timelimit value=\"999999000\" />\
                <!-- Зональное ограничение на начало езды. Проверяется один раз в начале программы -->\
                <constraint checkOnce=\"true\" failMessage=\"Робот должен находиться в синем квадрате перед запуском!\">\
                        <conditions glue=\"or\">\
                        </conditions>\
                </constraint>\
        </constraints>\
</root>\
"

FIELD_FINISH_STR = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
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
                <robot id=\"trikKitRobot\" position=\"0:0\" direction=\"0\">\
                        <sensors>\
                        </sensors>\
                        <startPosition id=\"{robot1}\" x=\"25\" y=\"25\" direction=\"0\" />\
                        <wheels left=\"M3###output###М3###\" right=\"M4###output###М4###\" />\
                </robot>\
        </robots>\
        <constraints>\
                <!-- Лимит на выполнение программы (30 секунд) -->\
                <timelimit value=\"999999000\" />\
                <!-- Событие, проверяющее не заехал ли робот в зону финиша -->\
                <event settedUpInitially=\"true\">\
                        <condition>\
                                <timer timeout=\"100\" forceDropOnTimeout=\"true\" />\
                        </condition>\
                        <trigger>\
                                <setUp id=\"finish checker\" />\
                        </trigger>\
                </event>\
                <event id=\"finish checker\" settedUpInitially=\"false\">\
                        <conditions glue=\"or\">\
                        </conditions>\
                        <trigger>\
                                <success />\
                        </trigger>\
                </event>\
        </constraints>\
</root>\
"