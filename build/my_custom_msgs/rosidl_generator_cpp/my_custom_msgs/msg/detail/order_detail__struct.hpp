// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_custom_msgs:msg/OrderDetail.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_custom_msgs__msg__OrderDetail __attribute__((deprecated))
#else
# define DEPRECATED__my_custom_msgs__msg__OrderDetail __declspec(deprecated)
#endif

namespace my_custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct OrderDetail_
{
  using Type = OrderDetail_<ContainerAllocator>;

  explicit OrderDetail_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->order_detail_id = 0ul;
      this->menu_name = "";
      this->table_num = 0ul;
    }
  }

  explicit OrderDetail_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : menu_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->order_detail_id = 0ul;
      this->menu_name = "";
      this->table_num = 0ul;
    }
  }

  // field types and members
  using _order_detail_id_type =
    uint32_t;
  _order_detail_id_type order_detail_id;
  using _menu_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _menu_name_type menu_name;
  using _table_num_type =
    uint32_t;
  _table_num_type table_num;

  // setters for named parameter idiom
  Type & set__order_detail_id(
    const uint32_t & _arg)
  {
    this->order_detail_id = _arg;
    return *this;
  }
  Type & set__menu_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->menu_name = _arg;
    return *this;
  }
  Type & set__table_num(
    const uint32_t & _arg)
  {
    this->table_num = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_custom_msgs::msg::OrderDetail_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_custom_msgs::msg::OrderDetail_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_custom_msgs__msg__OrderDetail
    std::shared_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_custom_msgs__msg__OrderDetail
    std::shared_ptr<my_custom_msgs::msg::OrderDetail_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const OrderDetail_ & other) const
  {
    if (this->order_detail_id != other.order_detail_id) {
      return false;
    }
    if (this->menu_name != other.menu_name) {
      return false;
    }
    if (this->table_num != other.table_num) {
      return false;
    }
    return true;
  }
  bool operator!=(const OrderDetail_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct OrderDetail_

// alias to use template instance with default allocator
using OrderDetail =
  my_custom_msgs::msg::OrderDetail_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__STRUCT_HPP_
