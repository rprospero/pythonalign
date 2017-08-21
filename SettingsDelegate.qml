import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import PythonAlign 1.0

Frame {
    signal scriptChanged
    onScriptChanged: saveButtonLabel.text = "Save"
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
	    contentItem: Text {
		id: saveButtonLabel
		text: "Save"
		color: runmodels.valid ? "black" : "red"
		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter
		elide: Text.ElideRight
	    }
	    Layout.fillWidth: true
	    onClicked: {
		if (runmodels.valid) {
		    saveDialog.open()
		}
	    }
	}
	FileDialog {
	    id: saveDialog
	    onAccepted: {
		runmodels.save(fileUrl)
	    }
	}
    }
}
