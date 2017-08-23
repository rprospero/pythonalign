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
    property url image
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
		source: image
		fillMode: Image.PreserveAspectFit
		anchors.horizontalCenter: parent.horizontalCenter
		anchors.verticalCenter: parent.verticalCenter
		transform: Translate {
		    x:translation.x;
		    y:translation.y;
		}
	    }
	    transform: Rotation {
		id: turn;
		angle: base.angle
	    }
	}
	transform: Scale {
	    id: sizer;
	    xScale: base.scale;
	    yScale: base.scale;
	}
    }
}
