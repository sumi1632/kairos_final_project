// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_custom_msgs:msg/UpdateStatus.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__BUILDER_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_custom_msgs/msg/detail/update_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_custom_msgs
{

namespace msg
{

namespace builder
{

class Init_UpdateStatus_status
{
public:
  explicit Init_UpdateStatus_status(::my_custom_msgs::msg::UpdateStatus & msg)
  : msg_(msg)
  {}
  ::my_custom_msgs::msg::UpdateStatus status(::my_custom_msgs::msg::UpdateStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_msgs::msg::UpdateStatus msg_;
};

class Init_UpdateStatus_id
{
public:
  Init_UpdateStatus_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_UpdateStatus_status id(::my_custom_msgs::msg::UpdateStatus::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_UpdateStatus_status(msg_);
  }

private:
  ::my_custom_msgs::msg::UpdateStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_msgs::msg::UpdateStatus>()
{
  return my_custom_msgs::msg::builder::Init_UpdateStatus_id();
}

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__BUILDER_HPP_
