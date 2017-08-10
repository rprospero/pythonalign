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
	    Image {
		id: original
		source: "./img.jpg"
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.left: anchors.right
		width: parent.width/2
		AlignData {
		    id: alignment
		    anchors.fill: parent
		    p1: Qt.point(0.1, 0.1)
		    p2: Qt.point(0.9, 0.1)
		    p3: Qt.point(0.9, 0.9)
		    p4: Qt.point(0.1, 0.9)
		    MouseArea {
			anchors.fill: parent
			hoverEnabled: true
			onPressed: alignment.select(mouse.x/width, mouse.y/height);
			onPositionChanged: {
			    if(mouse.buttons != 0){
				alignment.select(mouse.x/width, mouse.y/height)
			    }
			}
		    }
		}
	    }
	    Rectangle {
		id: twisted
		color: "green"
		clip: true
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		Text{ text:"world"}
		Item {
		    Image {
			source: "./img.jpg"
			transform: Rotation {origin.x: 256; origin.y:256; angle: 45}
		    }
		    transform: Scale {origin.x: 256; origin.y:256; xScale: 2; yScale: 2}
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
