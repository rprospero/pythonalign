import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import PythonAlign 1.0

Frame {
    GridLayout {
	anchors.fill: parent
	columns: 4
	Text {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    text: "Horizontal Command"
	}
	Frame {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    TextEdit {
		anchors.fill: parent
		focus: true
		text: runmodels.horizontalCommand
		onEditingFinished: runmodels.horizontalCommand = text
	    }
	}
	Text {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    text: "Vertical Command"
	}
	Frame {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    TextEdit {
		anchors.fill:parent
		focus: true
		text: runmodels.verticalCommand
		onEditingFinished: runmodels.verticalCommand = text
	    }
	}
	Text {
	    text: "Frame Width"
	}
	TextField {
	    Layout.fillWidth: true
	    text: runmodels.frameWidth
	    onTextEdited: runmodels.frameWidth = parseFloat(text)
	}
	Text {
	    text: "Frame Height"
	}
	TextField {
	    Layout.fillWidth: true
	    text: runmodels.frameHeight
	    onTextEdited: runmodels.frameHeight = parseFloat(text)
	}
	Button {
	    text: "Save"
	    Layout.fillWidth: true
	    onClicked: runmodels.save()
	}
	TextField {
	    text: runmodels.scriptPath
	    Layout.fillWidth: true
	    Layout.columnSpan: 3
	}
    }
}
