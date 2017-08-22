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
	    AlignData {
		id: alignment
		p1: Qt.point(0.1, 0.1)
		p2: Qt.point(0.9, 0.1)
		p3: Qt.point(0.9, 0.9)
		p4: Qt.point(0.1, 0.9)
		onRealigned: othercanvas.requestPaint()
	    }
	    Flickable {
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.left: anchors.right
		pressDelay: 2500
		clip: true
		width: parent.width/2
		contentWidth: original.width
		contentHeight: original.height
		Image {
		    id: original
		    source: "./img.jpg"
		    fillMode: Image.Pad
		    Canvas {
			id: othercanvas
			anchors.fill: parent
			onPaint: {
			    var ctx = getContext("2d")
			    ctx.reset()
			    ctx.strokeStyle = "red"
			    ctx.lineWidth = 2;
			    ctx.beginPath()
			    ctx.moveTo(alignment.p1.x*othercanvas.width,
				       alignment.p1.y*othercanvas.height)
			    ctx.lineTo(alignment.p2.x*othercanvas.width,
				       alignment.p2.y*othercanvas.height)
			    ctx.lineTo(alignment.p3.x*othercanvas.width,
				       alignment.p3.y*othercanvas.height)
			    ctx.lineTo(alignment.p4.x*othercanvas.width,
				       alignment.p4.y*othercanvas.height)
			    ctx.closePath()
			    ctx.stroke()

			}
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
	    }
	    Rectangle {
		color: "cyan"
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.right: parent.right
		width: parent.width/2
		ZoomImage {
		    id: twisted
		    imgWidth: original.width
		    imgHeight: original.height
		    angle: alignment.angle
		    scale: alignment.scale
		    translation: alignment.translate
		}
	    }
	}
	Item {
	    Rectangle {
		color: "cyan"
		anchors.top: parent.top
		anchors.bottom: parent.bottom
		anchors.left: parent.left
		width: parent.width/2
		ZoomImage {
		    id: canvas_image
		    imgWidth: original.width
		    imgHeight: original.height
		    angle: alignment.angle
		    scale: alignment.scale
		    translation: alignment.translate
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
		clip: true
	    }
	}
	Item {
	    Flickable {
		id: scriptFlick
		anchors.left: parent.left
		anchors.right: parent.right
		anchors.top: parent.top
		anchors.bottom: settings.top
		clip: true
		contentHeight: scriptText.height
		contentWidth: scriptText.width
		TextArea {
		    id: scriptText
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
	Item {
	}
    }
}
