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
    Text {
	text: position.title
	Layout.columnSpan: 3
	Layout.fillWidth: true
    }
    Text {text: "top"}
    Text {
	text: position.top
	Layout.fillWidth: true
    }
    Text {text: "left"}
    Text {
	text: position.left
	Layout.fillWidth: true
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
