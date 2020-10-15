/**
 * Orthanc - A Lightweight, RESTful DICOM Store
 * Copyright (C) 2012-2016 Sebastien Jodogne, Medical Physics
 * Department, University Hospital of Liege, Belgium
 * Copyright (C) 2017-2020 Osimis S.A., Belgium
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program. If not, see
 * <http://www.gnu.org/licenses/>.
 **/


#pragma once

#include "JobOperationValue.h"

#include "../../Compatibility.h"  // For ORTHANC_OVERRIDE

#include <string>

namespace Orthanc
{
  class ORTHANC_PUBLIC StringOperationValue : public JobOperationValue
  {
  private:
    std::string  content_;

  public:
    explicit StringOperationValue(const std::string& content) :
      JobOperationValue(JobOperationValue::Type_String),
      content_(content)
    {
    }

    virtual JobOperationValue* Clone() const ORTHANC_OVERRIDE
    {
      return new StringOperationValue(content_);
    }

    const std::string& GetContent() const
    {
      return content_;
    }

    virtual void Serialize(Json::Value& target) const ORTHANC_OVERRIDE
    {
      target = Json::objectValue;
      target["Type"] = "String";
      target["Content"] = content_;
    }
  };
}