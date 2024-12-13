// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:srv/ReceiveOrder.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__BUILDER_HPP_
#define CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/srv/detail/receive_order__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace srv
{

namespace builder
{

class Init_ReceiveOrder_Request_id
{
public:
  Init_ReceiveOrder_Request_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::srv::ReceiveOrder_Request id(::custom_msgs::srv::ReceiveOrder_Request::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::srv::ReceiveOrder_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::srv::ReceiveOrder_Request>()
{
  return custom_msgs::srv::builder::Init_ReceiveOrder_Request_id();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace srv
{

namespace builder
{

class Init_ReceiveOrder_Response_details
{
public:
  Init_ReceiveOrder_Response_details()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::srv::ReceiveOrder_Response details(::custom_msgs::srv::ReceiveOrder_Response::_details_type arg)
  {
    msg_.details = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::srv::ReceiveOrder_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::srv::ReceiveOrder_Response>()
{
  return custom_msgs::srv::builder::Init_ReceiveOrder_Response_details();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__BUILDER_HPP_
