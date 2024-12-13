// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:msg/UpdateStatus.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_H_
#define CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'status'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/UpdateStatus in the package custom_msgs.
typedef struct custom_msgs__msg__UpdateStatus
{
  uint32_t id;
  rosidl_runtime_c__String status;
} custom_msgs__msg__UpdateStatus;

// Struct for a sequence of custom_msgs__msg__UpdateStatus.
typedef struct custom_msgs__msg__UpdateStatus__Sequence
{
  custom_msgs__msg__UpdateStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__msg__UpdateStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_H_
