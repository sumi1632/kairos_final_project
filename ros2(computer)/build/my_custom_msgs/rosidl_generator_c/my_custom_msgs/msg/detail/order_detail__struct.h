// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_custom_msgs:msg/OrderDetail.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_H_
#define MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'menu_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/OrderDetail in the package my_custom_msgs.
typedef struct my_custom_msgs__msg__OrderDetail
{
  uint32_t order_detail_id;
  rosidl_runtime_c__String menu_name;
  uint32_t table_num;
} my_custom_msgs__msg__OrderDetail;

// Struct for a sequence of my_custom_msgs__msg__OrderDetail.
typedef struct my_custom_msgs__msg__OrderDetail__Sequence
{
  my_custom_msgs__msg__OrderDetail * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_custom_msgs__msg__OrderDetail__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_H_
