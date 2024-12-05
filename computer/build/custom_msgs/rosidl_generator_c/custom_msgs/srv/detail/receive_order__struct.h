// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:srv/ReceiveOrder.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_
#define CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/ReceiveOrder in the package custom_msgs.
typedef struct custom_msgs__srv__ReceiveOrder_Request
{
  uint32_t id;
} custom_msgs__srv__ReceiveOrder_Request;

// Struct for a sequence of custom_msgs__srv__ReceiveOrder_Request.
typedef struct custom_msgs__srv__ReceiveOrder_Request__Sequence
{
  custom_msgs__srv__ReceiveOrder_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__srv__ReceiveOrder_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'details'
#include "custom_msgs/msg/detail/order_detail__struct.h"

/// Struct defined in srv/ReceiveOrder in the package custom_msgs.
typedef struct custom_msgs__srv__ReceiveOrder_Response
{
  custom_msgs__msg__OrderDetail__Sequence details;
} custom_msgs__srv__ReceiveOrder_Response;

// Struct for a sequence of custom_msgs__srv__ReceiveOrder_Response.
typedef struct custom_msgs__srv__ReceiveOrder_Response__Sequence
{
  custom_msgs__srv__ReceiveOrder_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__srv__ReceiveOrder_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_H_
