import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Rectangle {
    id: base
    property real scale
    property real angle
    property point translation
    property real imgWidth
    property real imgHeight
    clip: true
    width: Math.min(parent.width, parent.height)
    height: Math.min(parent.width, parent.height)
    Item {
	anchors.horizontalCenter: parent.horizontalCenter
	anchors.verticalCenter: parent.verticalCenter
	Item {
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.verticalCenter: parent.verticalCenter
	    Image {
		id: ref
		source: "./img.jpg"
		fillMode: Image.PreserveAspectFit
		anchors.horizontalCenter: parent.horizontalCenter
		anchors.verticalCenter: parent.verticalCenter
		transform: Translate {
		    x:translation.x * imgWidth;
		    y:translation.y * imgHeight;
		}
	    }
	    transform: Rotation {
		id: turn; origin.x: parent.horizontalCenter;
		origin.y:parent.verticalCenter; angle: base.angle
	    }
	}
	transform: Scale {
	    id: sizer;
	    origin.x: ref.horizontalCenter;
	    origin.y: ref.verticalCenter;
	    xScale: base.scale*width/imgHeight;
	    yScale: base.scale*height/imgWidth;
	}
    }
}
