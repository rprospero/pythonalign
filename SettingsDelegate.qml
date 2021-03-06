import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import PythonAlign 1.0

Frame {
    signal exportScript(url fileUrl)
    signal load(url fileUrl)
    signal save(url fileUrl)
    property url image
    property string angleCommand
    property string horizontalCommand
    property string verticalCommand
    property real frameWidth
    property real frameHeight
    property real origin
    property bool valid
    GridLayout {
	anchors.fill: parent
	columns: 4
	Text {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    text: "Angle Header Command"
	}
	Frame {
	    Layout.fillWidth: true
	    Layout.fillHeight: true
	    Layout.columnSpan: 4
	    TextEdit {
		anchors.fill: parent
		focus: true
		text: angleCommand
		onTextChanged: {
		    angleCommand = text
		    console.log(angleCommand)
		}
	    }
	}
	Text {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    text: "Horizontal Command"
	}
	Frame {
	    Layout.fillWidth: true
	    Layout.fillHeight: true
	    Layout.columnSpan: 4
	    TextEdit {
		anchors.fill: parent
		focus: true
		text: horizontalCommand
		onTextChanged: horizontalCommand = text
	    }
	}
	Text {
	    Layout.fillWidth: true
	    Layout.columnSpan: 4
	    text: "Vertical Command"
	}
	Frame {
	    Layout.fillWidth: true
	    Layout.fillHeight: true
	    Layout.columnSpan: 4
	    TextEdit {
		anchors.fill:parent
		focus: true
		text: verticalCommand
		onTextChanged: verticalCommand = text
	    }
	}
	Text {
	    text: "Frame Width"
	}
	TextField {
	    Layout.fillWidth: true
	    text: frameWidth
	    onTextEdited: {
		var temp = parseFloat(text)
		if(!isNaN(temp)) {
		    frameWidth = temp
		}
	    }
	}
	Text {
	    text: "Frame Height"
	}
	TextField {
	    Layout.fillWidth: true
	    text: frameHeight
	    onTextEdited: {
		var temp = parseFloat(text)
		if(!isNaN(temp)) {
		    frameHeight = temp
		}
	    }
	}
	Text {
	    text: "Horizontal Origin"
	}
	TextField {
	    Layout.fillWidth: true
	    text: origin
	    Layout.columnSpan: 3
	    onTextEdited: {
		var temp = parseFloat(text)
		if(!isNaN(temp)) {
		    origin = temp
		}
	    }
	}
	Button {
	    contentItem: Text {
		text: "Export Script"
		color: valid ? "black" : "red"
		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter
		elide: Text.ElideRight
	    }
	    Layout.fillWidth: true
	    onClicked: {
		if (valid) {
		    exportDialog.open()
		}
	    }
	    FileDialog {
		id: exportDialog
		title: "Export the spec macros"
		nameFilters: ["Spec Macros (*.mac)"];
		selectExisting: false
		onAccepted: exportScript(fileUrl)
	    }
	}
	Button {
	    text: "Load Image"
	    Layout.fillWidth: true
	    onClicked: imageDialog.open()
	    FileDialog {
		id: imageDialog
		nameFilters: ["Jpeg (*.jpg, *.jpeg, *.JPG)", "Portable Network Graphcs (*.png)"]
		title: "Load Sample image"
		selectExisting: true
		onAccepted: image = fileUrl
	    }
	}
	Button {
	    text: "Load Settings"
	    Layout.fillWidth: true
	    onClicked: {
		loadDialog.open()
	    }
	    FileDialog {
		id: loadDialog
		nameFilters: ["JSON files (*.json)"];
		title: "Load a previously saved set of runs"
		selectExisting: true
		onAccepted: load(fileUrl)
	    }
	}
	Button {
	    text: "Save Settings"
	    Layout.fillWidth: true
	    onClicked: {
		saveDialog.open()
	    }
	    FileDialog {
		id: saveDialog
		nameFilters: ["JSON files (*.json)"];
		title: "Save the current set of runs"
		selectExisting: false
		onAccepted: save(fileUrl)
	    }
	}
    }
}
