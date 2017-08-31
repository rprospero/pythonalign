import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import PythonAlign 1.0

GridLayout {
    id: base
    width: parent.width
    columns: 2
    Text {
	text: "Title"
	color: run.valid ? "black" : "red"
    }
}
