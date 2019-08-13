#include "RunModel.h"

RunModel::RunModel(QObject* parent) : QObject(parent) {}

QString RunModel::script() {
  return QString("This is my script");
}

double RunModel::frameHeight() { return m_frameHeight; }
void RunModel::setFrameHeight(double w) {
  if (w == m_frameHeight) return;
  m_frameHeight = w;
}

double RunModel::frameWidth() { return m_frameWidth; }
void RunModel::setFrameWidth(double w) {
  if (w == m_frameWidth) return;
  m_frameWidth = w;
}

QString RunModel::horizontalCommand() { return m_horizontalCommand; }
void RunModel::setHorizontalCommand(QString w) {
  if (w == m_horizontalCommand) return;
  m_horizontalCommand = w;
}

QString RunModel::verticalCommand() { return m_verticalCommand; }
void RunModel::setVerticalCommand(QString w) {
  if (w == m_verticalCommand) return;
  m_verticalCommand = w;
}
