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

#include "../Enumerations.h"

#include <string>
#include <boost/noncopyable.hpp>

namespace Orthanc
{
  class IHttpOutputStream : public boost::noncopyable
  {
  public:
    virtual ~IHttpOutputStream()
    {
    }

    virtual void OnHttpStatusReceived(HttpStatus status) = 0;

    virtual void Send(bool isHeader, const void* buffer, size_t length) = 0;

    // Disable HTTP keep alive for this single HTTP connection. Must
    // be called before sending the "HTTP/1.1 200 OK" header.
    virtual void DisableKeepAlive() = 0;
  };
}
