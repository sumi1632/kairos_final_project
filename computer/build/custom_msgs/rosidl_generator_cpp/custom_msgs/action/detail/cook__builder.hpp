// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:action/Cook.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__ACTION__DETAIL__COOK__BUILDER_HPP_
#define CUSTOM_MSGS__ACTION__DETAIL__COOK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/action/detail/cook__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_Goal_menu_name
{
public:
  Init_Cook_Goal_menu_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Cook_Goal menu_name(::custom_msgs::action::Cook_Goal::_menu_name_type arg)
  {
    msg_.menu_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_Goal>()
{
  return custom_msgs::action::builder::Init_Cook_Goal_menu_name();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_Result_cook_result
{
public:
  Init_Cook_Result_cook_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Cook_Result cook_result(::custom_msgs::action::Cook_Result::_cook_result_type arg)
  {
    msg_.cook_result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_Result>()
{
  return custom_msgs::action::builder::Init_Cook_Result_cook_result();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_Feedback_cook_status
{
public:
  Init_Cook_Feedback_cook_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Cook_Feedback cook_status(::custom_msgs::action::Cook_Feedback::_cook_status_type arg)
  {
    msg_.cook_status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_Feedback>()
{
  return custom_msgs::action::builder::Init_Cook_Feedback_cook_status();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_SendGoal_Request_goal
{
public:
  explicit Init_Cook_SendGoal_Request_goal(::custom_msgs::action::Cook_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Cook_SendGoal_Request goal(::custom_msgs::action::Cook_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_SendGoal_Request msg_;
};

class Init_Cook_SendGoal_Request_goal_id
{
public:
  Init_Cook_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Cook_SendGoal_Request_goal goal_id(::custom_msgs::action::Cook_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Cook_SendGoal_Request_goal(msg_);
  }

private:
  ::custom_msgs::action::Cook_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_SendGoal_Request>()
{
  return custom_msgs::action::builder::Init_Cook_SendGoal_Request_goal_id();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_SendGoal_Response_stamp
{
public:
  explicit Init_Cook_SendGoal_Response_stamp(::custom_msgs::action::Cook_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Cook_SendGoal_Response stamp(::custom_msgs::action::Cook_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_SendGoal_Response msg_;
};

class Init_Cook_SendGoal_Response_accepted
{
public:
  Init_Cook_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Cook_SendGoal_Response_stamp accepted(::custom_msgs::action::Cook_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Cook_SendGoal_Response_stamp(msg_);
  }

private:
  ::custom_msgs::action::Cook_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_SendGoal_Response>()
{
  return custom_msgs::action::builder::Init_Cook_SendGoal_Response_accepted();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_GetResult_Request_goal_id
{
public:
  Init_Cook_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Cook_GetResult_Request goal_id(::custom_msgs::action::Cook_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_GetResult_Request>()
{
  return custom_msgs::action::builder::Init_Cook_GetResult_Request_goal_id();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_GetResult_Response_result
{
public:
  explicit Init_Cook_GetResult_Response_result(::custom_msgs::action::Cook_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Cook_GetResult_Response result(::custom_msgs::action::Cook_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_GetResult_Response msg_;
};

class Init_Cook_GetResult_Response_status
{
public:
  Init_Cook_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Cook_GetResult_Response_result status(::custom_msgs::action::Cook_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Cook_GetResult_Response_result(msg_);
  }

private:
  ::custom_msgs::action::Cook_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_GetResult_Response>()
{
  return custom_msgs::action::builder::Init_Cook_GetResult_Response_status();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Cook_FeedbackMessage_feedback
{
public:
  explicit Init_Cook_FeedbackMessage_feedback(::custom_msgs::action::Cook_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Cook_FeedbackMessage feedback(::custom_msgs::action::Cook_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Cook_FeedbackMessage msg_;
};

class Init_Cook_FeedbackMessage_goal_id
{
public:
  Init_Cook_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Cook_FeedbackMessage_feedback goal_id(::custom_msgs::action::Cook_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Cook_FeedbackMessage_feedback(msg_);
  }

private:
  ::custom_msgs::action::Cook_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Cook_FeedbackMessage>()
{
  return custom_msgs::action::builder::Init_Cook_FeedbackMessage_goal_id();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__ACTION__DETAIL__COOK__BUILDER_HPP_
