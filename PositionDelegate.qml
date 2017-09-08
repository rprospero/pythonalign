import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import PythonAlign 1.0

GridLayout {
    id: base
    width: parent.width
    columns: 4
    Text {
	text: "Title"
    }
    TextField {
	text: position.title
	Layout.columnSpan: 3
	Layout.fillWidth: true
	onTextEdited: position.title = text
    }
    Text {text: "top"}
    TextField {
	text: position.top.toFixed(4)
	Layout.fillWidth: true
	onTextEdited: position.top = parseFloat(text)
    }
    Text {text: "left"}
    TextField {
	text: position.left.toFixed(4)
	Layout.fillWidth: true
	onTextEdited: position.left = parseFloat(text)
    }
    Button {
	Layout.columnSpan: 4
	Layout.fillWidth: true
	text: "Delete"
	onClicked: {
	    positionModel.remove(index);
	}
    }
}
