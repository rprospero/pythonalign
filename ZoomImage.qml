import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Rectangle {
    id: base
    property real scale
    property real angle
    property real imgWidth
    property real imgHeight
    color: "green"
    clip: true
    Item {
	anchors.horizontalCenter: parent.horizontalCenter
	anchors.verticalCenter: parent.verticalCenter
	Image {
	    id: ref
	    width: imgWidth
	    height: imgHeight
	    source: "./img.jpg"
	    anchors.horizontalCenter: parent.horizontalCenter
	    anchors.verticalCenter: parent.verticalCenter
	    transform: Rotation {
		id: turn; origin.x: parent.horizontalCenter;
		origin.y:parent.verticalCenter; angle: base.angle}
	}
	transform: Scale {
	    id: sizer;
	    origin.x: ref.horizontalCenter;
	    origin.y: ref.verticalCenter;
	    xScale: base.scale;
	    yScale: base.scale;
	}
    }
}
