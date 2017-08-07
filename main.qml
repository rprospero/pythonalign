import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import PythonAlign 1.0

ApplicationWindow {
    TabBar {
	id: bar
	width: parent.width
	TabButton {
	    text: "Alignment"
	}
	TabButton {
	    text: "Runs"
	}
	TabButton {
	    text: "Script"
	}
    }
    StackLayout {
	id: tabview
	currentIndex: bar.currentIndex
	anchors.top: bar.bottom
	anchors.bottom: parent.bottom
	width: parent.width
	Item {
	    Rectangle {
		color: "black"
		anchors.fill: parent
		Text{ text:"Hello"}
		AlignData {
		    id: alignment
		    anchors.fill: parent
		    antialiasing: true
		}
	    }
	}
	Item {
	    Rectangle {
		color: "green"
		anchors.fill: parent
	    }
	}
	Item {
	    Rectangle {
		color: "blue"
		anchors.fill: parent
	    }
	}
    }
}
