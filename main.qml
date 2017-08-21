import QtQuick 2.7
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
		horizontalCommand:  "umv sav {starty}\nfor(i=0;i<{frameCount};i+=1)\n{{\n\ty={startx}+i*{stepSize}\n\tumv sah y\n\tccdacq_nodark {time} \"{title}\"\n}}"
		verticalCommand:  "umv sah {startx}\nccdtrans sav {starty} {stopy} {frameCount} {time} {sleep} \"{title}\" {ndark} 1"
		frameWidth: 25
		frameHeight: 25
	    }
	    ListView {
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		model: runmodels
		delegate: RunDelegate {}
	    }
	}
	Item {
	    Rectangle {
		color: "white"
		anchors.left: parent.left
		anchors.right: parent.right
		anchors.top: parent.top
		anchors.bottom: settings.top
		TextArea {
		    anchors.fill:parent
		    text: runmodels.script
		    selectByKeyboard: true
		    selectByMouse: true
		}
	    }
	    SettingsDelegate {
		id: settings
		anchors.left: parent.left
		anchors.right: parent.right
		anchors.bottom: parent.bottom
	    }
	}
    }
}
