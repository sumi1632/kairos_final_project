// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_custom_msgs:srv/ReceiveOrder.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_
#define MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/ReceiveOrder in the package my_custom_msgs.
typedef struct my_custom_msgs__srv__ReceiveOrder_Request
{
  uint32_t id;
} my_custom_msgs__srv__ReceiveOrder_Request;

// Struct for a sequence of my_custom_msgs__srv__ReceiveOrder_Request.
typedef struct my_custom_msgs__srv__ReceiveOrder_Request__Sequence
{
  my_custom_msgs__srv__ReceiveOrder_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_msgs__srv__ReceiveOrder_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'details'
#include "my_custom_msgs/msg/detail/order_detail__struct.h"

/// Struct defined in srv/ReceiveOrder in the package my_custom_msgs.
typedef struct my_custom_msgs__srv__ReceiveOrder_Response
{
  my_custom_msgs__msg__OrderDetail__Sequence details;
} my_custom_msgs__srv__ReceiveOrder_Response;

// Struct for a sequence of my_custom_msgs__srv__ReceiveOrder_Response.
typedef struct my_custom_msgs__srv__ReceiveOrder_Response__Sequence
{
  my_custom_msgs__srv__ReceiveOrder_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_msgs__srv__ReceiveOrder_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_
