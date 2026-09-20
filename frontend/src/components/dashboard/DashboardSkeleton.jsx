import Card from "../common/Card";
import Skeleton from "../common/Skeleton";
import DashboardGrid from "./DashboardGrid";

export default function DashboardSkeleton() {

    return (

        <DashboardGrid>

            <div className="col-span-4">

                <Card className="flex flex-col items-center text-center">

                    <Skeleton className="h-5 w-32" />

                    <Skeleton className="h-40 w-40 rounded-full mt-6" />

                    <Skeleton className="h-5 w-24 mt-6" />

                </Card>

            </div>

            <div className="col-span-8 grid grid-cols-3 gap-6">

                {[0, 1, 2].map((i) => (

                    <Card key={i}>

                        <Skeleton className="h-4 w-20" />

                        <Skeleton className="h-8 w-28 mt-3" />

                    </Card>

                ))}

                <div className="col-span-3">

                    <Card>

                        <Skeleton className="h-6 w-40" />

                        <Skeleton className="h-4 w-full mt-4" />
                        <Skeleton className="h-4 w-3/4 mt-2" />

                    </Card>

                </div>

            </div>

            <div className="col-span-5">

                <Card>

                    <Skeleton className="h-6 w-24" />

                    <Skeleton className="h-16 w-full mt-6" />
                    <Skeleton className="h-16 w-full mt-4" />

                </Card>

            </div>

            <div className="col-span-7">

                <Card>

                    <Skeleton className="h-6 w-48" />

                    <div className="mt-8 flex gap-8 items-center">

                        <Skeleton className="h-44 w-44 rounded-full shrink-0" />

                        <div className="flex-1 space-y-6">

                            {[0, 1, 2].map((i) => (
                                <Skeleton key={i} className="h-8 w-full" />
                            ))}

                        </div>

                    </div>

                </Card>

            </div>

            <div className="col-span-12">

                <Card>

                    <Skeleton className="h-6 w-32" />

                    <div className="mt-8 space-y-6">

                        {[0, 1, 2].map((i) => (
                            <Skeleton key={i} className="h-6 w-full" />
                        ))}

                    </div>

                </Card>

            </div>

        </DashboardGrid>

    );

}