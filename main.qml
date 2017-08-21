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

			for(var i=0;i<runmodels.count;i++) {
			    var run = runmodels.get(i)
			    if(run.selected){
				ctx.strokeStyle = "#00FFFF"
			    } else {
				ctx.strokeStyle = "red"
			    }
			    ctx.lineWidth = 2;
			    ctx.beginPath()
			    ctx.moveTo(run.startx*canvas.width,
				       run.starty*canvas.height)
			    ctx.lineTo(run.stopx*canvas.width,
				       run.stopy*canvas.height)
			    ctx.stroke()
			}
		    }
		}
		MouseArea {
		    anchors.fill: parent
		    hoverEnabled: true
		    onPressed: runmodels.append(mouse.x/width, mouse.y/height, 0.5, 0.5)
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
		model: runmodels
		delegate: Row {
		    width: parent.width
		    TextField {
			width: parent.width/5;
			text: run.startx.toFixed(4)
			onTextEdited: {
			    run.startx = parseFloat(text);
			    canvas.requestPaint()
			}
			onActiveFocusChanged: {
			    run.selected = !run.selected
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: run.starty.toFixed(4)
			onTextEdited: {
			    run.starty = parseFloat(text);
			    canvas.requestPaint()
			}
			onActiveFocusChanged: {
			    run.selected = !run.selected
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: run.stopx.toFixed(4)
			onTextEdited: {
			    run.stopx = parseFloat(text);
			    canvas.requestPaint()
			}
			onActiveFocusChanged: {
			    run.selected = !run.selected
			    canvas.requestPaint()
			}
		    }
		    TextField {
			width: parent.width/5;
			text: run.stopy.toFixed(4)
			onTextEdited: {
			    run.stopy = parseFloat(text);
			    canvas.requestPaint()
			}
			onActiveFocusChanged: {
			    run.selected = !run.selected
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
		color: "white"
		anchors.fill: parent
		TextArea {
		    anchors.fill:parent
		    text: runmodels.script
		    selectByKeyboard: true
		    selectByMouse: true
		}
	    }
	}
    }
}
