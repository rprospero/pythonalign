#include "PositionModel.h"

PositionModel::PositionModel(QObject* parent) : QObject(parent) {}

qreal PositionModel::width() {
  return m_width;
}

void PositionModel::setWidth(qreal w) {
  if (w == m_width) return;

  m_width = w;
}
