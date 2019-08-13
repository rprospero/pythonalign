#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include "RunModel.h"
#include "AlignData.h"
#include "PositionModel.h"



int main(int argc, char **argv) {
  QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

  QGuiApplication app(argc, argv);

  qmlRegisterType<RunModel>("PythonAlign", 1, 0, "RunModel");
  qmlRegisterType<AlignData>("PythonAlign", 1, 0, "AlignData");
  qmlRegisterType<PositionModel>("PythonAlign", 1, 0, "PositionModel");

  QQmlApplicationEngine engine;

  engine.load(QUrl(QStringLiteral("file:main.qml")));
  if (engine.rootObjects().isEmpty()) return -1;

  return app.exec();
}
