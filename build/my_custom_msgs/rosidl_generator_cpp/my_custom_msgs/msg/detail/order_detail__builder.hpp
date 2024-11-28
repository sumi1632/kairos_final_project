// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_custom_msgs:msg/OrderDetail.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__BUILDER_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_custom_msgs/msg/detail/order_detail__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_custom_msgs
{

namespace msg
{

namespace builder
{

class Init_OrderDetail_table_num
{
public:
  explicit Init_OrderDetail_table_num(::my_custom_msgs::msg::OrderDetail & msg)
  : msg_(msg)
  {}
  ::my_custom_msgs::msg::OrderDetail table_num(::my_custom_msgs::msg::OrderDetail::_table_num_type arg)
  {
    msg_.table_num = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_custom_msgs::msg::OrderDetail msg_;
};

class Init_OrderDetail_menu_name
{
public:
  explicit Init_OrderDetail_menu_name(::my_custom_msgs::msg::OrderDetail & msg)
  : msg_(msg)
  {}
  Init_OrderDetail_table_num menu_name(::my_custom_msgs::msg::OrderDetail::_menu_name_type arg)
  {
    msg_.menu_name = std::move(arg);
    return Init_OrderDetail_table_num(msg_);
  }

private:
  ::my_custom_msgs::msg::OrderDetail msg_;
};

class Init_OrderDetail_order_detail_id
{
public:
  Init_OrderDetail_order_detail_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OrderDetail_menu_name order_detail_id(::my_custom_msgs::msg::OrderDetail::_order_detail_id_type arg)
  {
    msg_.order_detail_id = std::move(arg);
    return Init_OrderDetail_menu_name(msg_);
  }

private:
  ::my_custom_msgs::msg::OrderDetail msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_custom_msgs::msg::OrderDetail>()
{
  return my_custom_msgs::msg::builder::Init_OrderDetail_order_detail_id();
}

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__BUILDER_HPP_
