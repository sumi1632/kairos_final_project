// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from my_custom_msgs:msg/OrderDetail.idl
// generated code does not contain a copyright notice
#include "my_custom_msgs/msg/detail/order_detail__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `menu_name`
#include "rosidl_runtime_c/string_functions.h"

bool
my_custom_msgs__msg__OrderDetail__init(my_custom_msgs__msg__OrderDetail * msg)
{
  if (!msg) {
    return false;
  }
  // order_detail_id
  // menu_name
  if (!rosidl_runtime_c__String__init(&msg->menu_name)) {
    my_custom_msgs__msg__OrderDetail__fini(msg);
    return false;
  }
  // table_num
  return true;
}

void
my_custom_msgs__msg__OrderDetail__fini(my_custom_msgs__msg__OrderDetail * msg)
{
  if (!msg) {
    return;
  }
  // order_detail_id
  // menu_name
  rosidl_runtime_c__String__fini(&msg->menu_name);
  // table_num
}

bool
my_custom_msgs__msg__OrderDetail__are_equal(const my_custom_msgs__msg__OrderDetail * lhs, const my_custom_msgs__msg__OrderDetail * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // order_detail_id
  if (lhs->order_detail_id != rhs->order_detail_id) {
    return false;
  }
  // menu_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->menu_name), &(rhs->menu_name)))
  {
    return false;
  }
  // table_num
  if (lhs->table_num != rhs->table_num) {
    return false;
  }
  return true;
}

bool
my_custom_msgs__msg__OrderDetail__copy(
  const my_custom_msgs__msg__OrderDetail * input,
  my_custom_msgs__msg__OrderDetail * output)
{
  if (!input || !output) {
    return false;
  }
  // order_detail_id
  output->order_detail_id = input->order_detail_id;
  // menu_name
  if (!rosidl_runtime_c__String__copy(
      &(input->menu_name), &(output->menu_name)))
  {
    return false;
  }
  // table_num
  output->table_num = input->table_num;
  return true;
}

my_custom_msgs__msg__OrderDetail *
my_custom_msgs__msg__OrderDetail__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__OrderDetail * msg = (my_custom_msgs__msg__OrderDetail *)allocator.allocate(sizeof(my_custom_msgs__msg__OrderDetail), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(my_custom_msgs__msg__OrderDetail));
  bool success = my_custom_msgs__msg__OrderDetail__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
my_custom_msgs__msg__OrderDetail__destroy(my_custom_msgs__msg__OrderDetail * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    my_custom_msgs__msg__OrderDetail__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
my_custom_msgs__msg__OrderDetail__Sequence__init(my_custom_msgs__msg__OrderDetail__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__OrderDetail * data = NULL;

  if (size) {
    data = (my_custom_msgs__msg__OrderDetail *)allocator.zero_allocate(size, sizeof(my_custom_msgs__msg__OrderDetail), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = my_custom_msgs__msg__OrderDetail__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        my_custom_msgs__msg__OrderDetail__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
my_custom_msgs__msg__OrderDetail__Sequence__fini(my_custom_msgs__msg__OrderDetail__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      my_custom_msgs__msg__OrderDetail__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

my_custom_msgs__msg__OrderDetail__Sequence *
my_custom_msgs__msg__OrderDetail__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_custom_msgs__msg__OrderDetail__Sequence * array = (my_custom_msgs__msg__OrderDetail__Sequence *)allocator.allocate(sizeof(my_custom_msgs__msg__OrderDetail__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = my_custom_msgs__msg__OrderDetail__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
my_custom_msgs__msg__OrderDetail__Sequence__destroy(my_custom_msgs__msg__OrderDetail__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    my_custom_msgs__msg__OrderDetail__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
my_custom_msgs__msg__OrderDetail__Sequence__are_equal(const my_custom_msgs__msg__OrderDetail__Sequence * lhs, const my_custom_msgs__msg__OrderDetail__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!my_custom_msgs__msg__OrderDetail__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
my_custom_msgs__msg__OrderDetail__Sequence__copy(
  const my_custom_msgs__msg__OrderDetail__Sequence * input,
  my_custom_msgs__msg__OrderDetail__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(my_custom_msgs__msg__OrderDetail);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    my_custom_msgs__msg__OrderDetail * data =
      (my_custom_msgs__msg__OrderDetail *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!my_custom_msgs__msg__OrderDetail__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          my_custom_msgs__msg__OrderDetail__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!my_custom_msgs__msg__OrderDetail__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
