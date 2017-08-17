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
			canvas_image.angle = alignment.angle;
			canvas_image.scale = alignment.scale;
			canvas_image.translation = alignment.translate;
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
		id: canvas_image
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.left: parent.left
		width: parent.width/2
		imgWidth: original.width
		imgHeight: original.height
		Canvas {
		    id: canvas
		    anchors.fill: parent
		    onPaint: {
			var ctx = getContext("2d")
			ctx.reset()

			ctx.lineWidth = 2;
			ctx.strokeStyle = "red"
			ctx.beginPath()
			for(var i=0;i<runmodels.count;i++) {
			    ctx.moveTo(runmodels.get(i).startx*canvas.width,
				       runmodels.get(i).starty*canvas.height)
			    ctx.lineTo(runmodels.get(i).stopx*canvas.width,
				       runmodels.get(i).stopy*canvas.height)
			}
			//ctx.closePath()
			ctx.stroke()
		    }
		}
		MouseArea {
		    anchors.fill: parent
		    hoverEnabled: true
		    onPressed: runmodels.append(0.5, 0.5, mouse.x/width, mouse.y/height)
		    onPositionChanged: {
			if(mouse.buttons != 0){
			    runmodels.update(mouse.x/width, mouse.y/height)
			    canvas.requestPaint()
			}
		    }
		}
	    }
	    RunModel {
		id: runmodels
	    }
	    ListView {
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		model: runmodels.runs
		delegate: Row {
		    width: parent.width
		    TextField {
			width: parent.width/5;
			text: startx
			onTextEdited: {
			    startx = text;
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: starty
			onTextEdited: {
			    starty = text;
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: stopx
			onTextEdited: {
			    stopx = text;
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: stopy
			onTextEdited: {
			    stopy = text;
			    canvas.requestPaint()
			}
		    }
		    Button {
			width: parent.width/5;
			text: "Delete"
			onClicked: {
			    runmodels.remove(index);
			    canvas.requestPaint()
			}
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
