# See https://pypi.org/project/centroid-tracker/ for implementation?

from dataclasses import dataclass, field
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
Point = tuple[int, int]


class TrackedObject:
    nextId = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.velocity = 0
        self.ticksMissing = 0
        self.id = self.__class__.nextId
        self.__class__.nextId += 1


class CentroidTracker:
    def __init__(self, maxAcceleration=10, maxDisappeared=50):
        """
        Tracks a point across space, taking into account its velocity
        :param maxAcceleration: in units of pixels/frame^2
        :param maxDisappeared: the maximum amount of frames that an object can be missing until deregistered
        """
        self.trackedObjects: OrderedDict[int, TrackedObject] = OrderedDict()

        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects: OrderedDict[int, Point] = OrderedDict()
        self.disappeared: OrderedDict[int, int] = OrderedDict()
        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappeared = maxDisappeared

    def register(self, centroid: Point):
        t = TrackedObject(*centroid)
        self.trackedObjects[t.id] = t

        # when registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID: int):
        del self.trackedObjects[objectID]

        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:  # TODO: can this be generalized?
            # loop over any existing tracked objects and mark them
            # as disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                # if we have reached a maximum number of consecutive
                # frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            # return early as there are no centroids or tracking info
            # to update
            return self.objects

        # initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i])
        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            # Shape: (# of object centroids, # of input centroids)
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            print(D)
            # in order to perform this matching we must (1) find the
            # smallest value in each row and then (2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value is at the *front* of the index
            # list
            rows: list[int] = D.min(axis=1).argsort()
            print(rows)
            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols: list[int] = D.argmin(axis=1)[rows]
            print(cols)


if __name__ == "__main__":
    tracker = CentroidTracker()
    tracker.register((0, 0))
    tracker.register((15, 15))
    tracker.update([(0, 0, 10, 10), (-5, -5, 6, 6)])
