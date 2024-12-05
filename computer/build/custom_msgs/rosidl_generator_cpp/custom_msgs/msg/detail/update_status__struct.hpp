// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msgs:msg/UpdateStatus.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_msgs__msg__UpdateStatus __attribute__((deprecated))
#else
# define DEPRECATED__custom_msgs__msg__UpdateStatus __declspec(deprecated)
#endif

namespace custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct UpdateStatus_
{
  using Type = UpdateStatus_<ContainerAllocator>;

  explicit UpdateStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ul;
      this->status = "";
    }
  }

  explicit UpdateStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ul;
      this->status = "";
    }
  }

  // field types and members
  using _id_type =
    uint32_t;
  _id_type id;
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;

  // setters for named parameter idiom
  Type & set__id(
    const uint32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msgs::msg::UpdateStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msgs::msg::UpdateStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::UpdateStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::UpdateStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msgs__msg__UpdateStatus
    std::shared_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msgs__msg__UpdateStatus
    std::shared_ptr<custom_msgs::msg::UpdateStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const UpdateStatus_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const UpdateStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct UpdateStatus_

// alias to use template instance with default allocator
using UpdateStatus =
  custom_msgs::msg::UpdateStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__STRUCT_HPP_
