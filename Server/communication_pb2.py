# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: communication.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x63ommunication.proto\"\x81\x01\n\x0cserver_input\x12\x0c\n\x04imgs\x18\x01 \x01(\x0c\x12\r\n\x05\x62\x61tch\x18\x02 \x01(\x05\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x0f\n\x07\x63hannel\x18\x05 \x01(\x05\x12\x11\n\tdata_type\x18\x06 \x01(\t\x12\x11\n\tclient_id\x18\x07 \x01(\t\"\x90\x01\n\rserver_output\x12\x19\n\x11\x62rand_recognition\x18\x01 \x01(\x0c\x12\x1e\n\x16\x62rand_labels_filenames\x18\x02 \x01(\x0c\x12\x12\n\nembeddings\x18\x03 \x01(\x0c\x12\r\n\x05width\x18\x04 \x01(\x05\x12\x0e\n\x06height\x18\x05 \x01(\x05\x12\x11\n\tdata_type\x18\x06 \x01(\t22\n\x02\x62r\x12,\n\tinference\x12\r.server_input\x1a\x0e.server_output\"\x00\x62\x06proto3')



_SERVER_INPUT = DESCRIPTOR.message_types_by_name['server_input']
_SERVER_OUTPUT = DESCRIPTOR.message_types_by_name['server_output']
server_input = _reflection.GeneratedProtocolMessageType('server_input', (_message.Message,), {
  'DESCRIPTOR' : _SERVER_INPUT,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:server_input)
  })
_sym_db.RegisterMessage(server_input)

server_output = _reflection.GeneratedProtocolMessageType('server_output', (_message.Message,), {
  'DESCRIPTOR' : _SERVER_OUTPUT,
  '__module__' : 'communication_pb2'
  # @@protoc_insertion_point(class_scope:server_output)
  })
_sym_db.RegisterMessage(server_output)

_BR = DESCRIPTOR.services_by_name['br']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SERVER_INPUT._serialized_start=24
  _SERVER_INPUT._serialized_end=153
  _SERVER_OUTPUT._serialized_start=156
  _SERVER_OUTPUT._serialized_end=300
  _BR._serialized_start=302
  _BR._serialized_end=352
# @@protoc_insertion_point(module_scope)
