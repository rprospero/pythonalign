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
		fillMode: Image.PreserveAspectFit
		width: parent.width/2
		AlignData {
		    id: alignment
		    anchors.fill: parent
		    onRealigned: {
			twisted.angle = alignment.angle;
			twisted.scale = alignment.scale;
			twisted.translation = alignment.translate;
			canvas.angle = alignment.angle;
			canvas.scale = alignment.scale;
			canvas.translation = alignment.translate;
		    }
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
	    ZoomImage {
		id: twisted
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		imgWidth: original.width
		imgHeight: original.height
	    }
	}
	Item {
	    ZoomImage {
		id: canvas
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.left: parent.left
		width: parent.width/2
		imgWidth: original.width
		imgHeight: original.height
		MouseArea {
		    anchors.fill: parent
		    hoverEnabled: true
		    onPressed: runmodels.append(
			{
			    "stopx": 0.5,
			    "stopy": 0.5,
			    "startx": mouse.x/width,
			    "starty":mouse.y/height
			}
		    )
		    onPositionChanged: {
			if(mouse.buttons != 0){
			    runmodels.setProperty(
				runmodels.count - 1,
				"stopx",
				mouse.x/width
			    )
			    runmodels.setProperty(
				runmodels.count - 1,
				"stopy",
				mouse.y/height
			    )
			}
		    }
		}
	    }
	    ListView {
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		model: ListModel {
		    id: runmodels
		    ListElement {
			startx: 0; starty: 0;
			stopx: 1; stopy: 1;
			index: 0;
		    }
		    ListElement {
			startx: 0.2; starty: 0.9;
			stopx: 0.8; stopy: 0.1;
			index: 1;
		    }
		}
		delegate: Row {
		    Text {
			width: 150
			text: startx
		    }
		    Text {
			width: 150
			text: starty
		    }
		    Text {
			width: 150
			text: stopx
		    }
		    Text {
			width: 150
			text: stopy
		    }
		    Button {
			text: "Delete"
		    }
		}
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
