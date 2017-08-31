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
	    onClicked: original.focus=true
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
	    Keys.onPressed: {
		switch (event.key) {
		case Qt.Key_Plus:
		case Qt.Key_Equal:
		    originzoom.xScale *= 1.1;
		    originzoom.yScale *= 1.1;
		    break;
		case Qt.Key_Minus:
		    originzoom.xScale *= 0.9;
		    originzoom.yScale *= 0.9;
		    break;
		case Qt.Key_Asterisk:
		    originzoom.xScale = 0.25;
		    originzoom.yScale = 0.25;
		    break;
		}
	    }
	    AlignData {
		id: alignment
		p1: Qt.point(400, 400)
		p2: Qt.point(2000, 400)
		p3: Qt.point(2000, 2000)
		p4: Qt.point(400, 2000)
		onRealigned: othercanvas.requestPaint()
		width: original.width
		height: original.height
		newsize: twisted.width
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
		focus:true
		Image {
		    id: original
		    source: settings.image
		    fillMode: Image.Pad
		    Canvas {
			id: othercanvas
			anchors.fill: parent
			onPaint: {
			    var ctx = getContext("2d")
			    ctx.reset()
			    ctx.strokeStyle = "red"
			    ctx.lineWidth = 8;
			    ctx.beginPath()
			    ctx.moveTo(alignment.p1.x, alignment.p1.y)
			    ctx.lineTo(alignment.p2.x, alignment.p2.y)
			    ctx.lineTo(alignment.p3.x, alignment.p3.y)
			    ctx.lineTo(alignment.p4.x, alignment.p4.y)
			    ctx.closePath()
			    ctx.stroke()

			}
			MouseArea {
			    anchors.fill: parent
			    hoverEnabled: true
			    onPressed: alignment.select(mouse.x, mouse.y);
			    onPositionChanged: {
				if(mouse.buttons != 0){
				    alignment.select(mouse.x, mouse.y)
				}
			    }
			}
		    }
		    transform: Scale {
			id: originzoom
			xScale: 0.25
			yScale: 0.25
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
		    image: settings.image
		    imgWidth: original.width
		    imgHeight: original.height
		    angle: alignment.angle
		    scale: alignment.scale
		    translation: alignment.translate
		    anchors.verticalCenter: parent.verticalCenter
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
		    image: settings.image
		    imgWidth: original.width
		    imgHeight: original.height
		    angle: alignment.angle
		    scale: alignment.scale
		    translation: alignment.translate
		    anchors.verticalCenter: parent.verticalCenter
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
		image: "./img.jpg"
		anchors.left: parent.left
		anchors.right: parent.right
		anchors.bottom: parent.bottom
		horizontalCommand: runmodels.horizontalCommand
		verticalCommand: runmodels.verticalCommand
		frameWidth: runmodels.frameWidth
		frameHeight: runmodels.frameHeight
		valid: runmodels.valid

		Binding {
		    target: runmodels;
		    property: "horizontalCommand";
		    value: settings.horizontalCommand
		}
		Binding {
		    target: runmodels;
		    property: "verticalCommand";
		    value: settings.verticalCommand
		}

		onExportScript: runmodels.export(fileUrl)
		onLoad: {
		    runmodels.load(fileUrl)
		    alignment.jsonString = runmodels.alignmentJson
		}
		onSave: runmodels.save(fileUrl, alignment.jsonString)
	    }
	}
    }
}
