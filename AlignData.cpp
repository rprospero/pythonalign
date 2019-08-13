#include "AlignData.h"

AlignData::AlignData(QObject* parent) : QObject(parent) {}

qreal AlignData::width() {
  return m_width;
}

void AlignData::setWidth(qreal w) {
  if (w == m_width) return;

  m_width = w;
}

qreal AlignData::height() {
  return m_height;
}

void AlignData::setHeight(qreal w) {
  if (w == m_height) return;

  m_height = w;
}

qreal AlignData::newsize() {
  return m_newsize;
}

void AlignData::setNewsize(qreal w) {
  if (w == m_newsize) return;

  m_newsize = w;
}

QPointF AlignData::p1() { return m_p1; }
void AlignData::setP1(QPointF p) {
  if (m_p1 == p) return;
  m_p1 = p;
}


QPointF AlignData::p2() { return m_p2; }
void AlignData::setP2(QPointF p) {
  if (m_p2 == p) return;
  m_p2 = p;
}

QPointF AlignData::p3() { return m_p3; }
void AlignData::setP3(QPointF p) {
  if (m_p3 == p) return;
  m_p3 = p;
}

QPointF AlignData::p4() { return m_p4; }
void AlignData::setP4(QPointF p) {
  if (m_p4 == p) return;
  m_p4 = p;
}
