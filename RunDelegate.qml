import QtQuick 2.1
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import PythonAlign 1.0

GridLayout {
    id: base
    width: parent.width
    columns: 4
    Text {
	text: "Title"
	color: run.valid ? "black" : "red"
    }
    TextField {
	text: run.title
	Layout.columnSpan: 3
	Layout.fillWidth: true
	onTextEdited: {
	    run.title = text
	}
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Start x"}
    TextField {
	text: (run.startx*runmodels.frameWidth).toFixed(4)
	onTextEdited: {
	    run.startx = parseFloat(text)/runmodels.frameWidth;
	    canvas.requestPaint()
	}
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Start y"}
    TextField {
	text: (run.starty*runmodels.frameHeight).toFixed(4)
	onTextEdited: {
	    run.starty = parseFloat(text)/runmodels.frameWidth;
	    canvas.requestPaint()
	}
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Stop x"}
    TextField {
	text: (run.stopx*runmodels.frameWidth).toFixed(4)
	onTextEdited: {
	    run.stopx = parseFloat(text)/runmodels.frameWidth;
	    canvas.requestPaint()
	}
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Stop y"}
    TextField {
	text: (run.stopy*runmodels.frameHeight).toFixed(4)
	onTextEdited: {
	    run.stopy = parseFloat(text)/runmodels.frameWidth;
	    canvas.requestPaint()
	}
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Step Size"}
    TextField {
	text: run.stepSize
	onTextEdited: run.stepSize = parseFloat(text)
	onActiveFocusChanged: {
	    run.selected = !run.selected
	    canvas.requestPaint()
	}
    }
    Text {text: "Position"}
    ComboBox {
    	model: positionModel
    	textRole: "display"
	editText: run.position
	onCurrentTextChanged: {
	    run.position = currentText
	}
    }
    Button {
	Layout.columnSpan: 4
	Layout.fillWidth: true
	text: "Delete"
	onClicked: {
	    runmodels.remove(index);
	    canvas.requestPaint()
	}
    }
}
